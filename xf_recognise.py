#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-7-13
import logging
import os
import socket
import threading
import urllib.parse
import urllib.request
import time
import json
import hashlib
import base64
import wave
from math import ceil

import config


class RcgCore(threading.Thread):
    def __init__(self, wav_file, timeout=600, x_appid=None, api_key=None):
        threading.Thread.__init__(self)
        self.wav_file = wav_file
        self.timeout = timeout
        self.x_appid = x_appid
        self.api_key = api_key
        self.result = None

    def run(self):
        with open(self.wav_file, 'rb') as f:   # 以二进制格式只读打开文件读取，bytes
            file_content = f.read()
        base64_audio = base64.b64encode(file_content)  # 参数是bytes类型，返回也是bytes类型
        body = urllib.parse.urlencode({'audio': base64_audio})
        url = config.XF_RCG_URL
        if self.x_appid is None:
            self.x_appid = config.XF_APP_ID
        if self.api_key is None:
            self.api_key = config.XF_RCG_API_KEY
        param = {"engine_type": config.XF_RCG_ENGINE_TYPE, "aue": "raw"}
        x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
        x_time = int(int(round(time.time() * 1000)) / 1000)

        # print(x_param)  # bytes
        x_checksum_content = self.api_key + str(x_time) + str(x_param, 'utf-8')
        x_checksum = hashlib.md5(x_checksum_content.encode('utf-8')).hexdigest()

        # 讯飞api说明：
        # 授权认证，调用接口需要将Appid，CurTime, Param和CheckSum信息放在HTTP请求头中；
        # 接口统一为UTF-8编码；
        # 接口支持http和https；
        # 请求方式为POST。
        x_header = {'X-Appid': self.x_appid,
                    'X-CurTime': x_time,
                    'X-Param': x_param,
                    'X-CheckSum': x_checksum}
        req = urllib.request.Request(url=url, data=body.encode('utf-8'), headers=x_header, method='POST')
        try:
            rst = urllib.request.urlopen(req, timeout=self.timeout)
            self.result = rst.read().decode('utf-8')
        except Exception as e:
            logging.info(e)

    def get_result(self):
        return self.result


def rcg(wav_file, timeout=600, segments=0, x_appid=None, api_key=None):
    with wave.open(wav_file, 'rb') as wf:
        params = wf.getparams()
        nchannels, sampwidth, framerate, nframes = params[:4]
        duration = nframes / framerate
        if segments == 0:  # if segments is not assigned manually, calculate segments count
            segments = ceil(duration / 60)
        if segments >= 2:  # cut wav into segments (average length)
            logging.debug("Cutting %s by into %d segments..." % (wav_file, segments))
            seg_length = ceil(duration / segments * framerate)  # how many frames per segment
            for i in range(segments):
                seg_filename = wav_file.split('.wav')[0] + '_rcg_seg_%d.wav' % i
                seg_data = wf.readframes(seg_length)
                with wave.open(seg_filename, 'wb') as seg:
                    seg.setnchannels(nchannels)
                    seg.setsampwidth(sampwidth)
                    seg.setframerate(framerate)
                    seg.writeframes(seg_data)
    if segments == 1:  # return is a 'str' object
        rcg_core = RcgCore(wav_file, timeout, x_appid, api_key)
        rcg_core.start()
        rcg_core.join()
        result = rcg_core.get_result()
        rcg_dict = json.loads(result)
        if rcg_dict.get('code') == '10105':
            print('IP错误, 请把下面的IP添加至讯飞云IP白名单并等待两分钟再试!!')
            print(rcg_dict.get('desc').strip('illegal access|illegal client_ip: '))  # no need to use replace here
            print()
            raise Exception('RCG IP Error')
        return result
    if segments >= 2:  # return is a 'dict' object
        threads = dict()
        results = {}

        for i in range(segments):
            seg_filename = wav_file.split('.wav')[0] + '_rcg_seg_%d.wav' % i
            threads[i] = RcgCore(seg_filename, timeout, x_appid, api_key)
            threads[i].start()

        for i in range(segments):
            threads[i].join()

        for i in range(segments):
            results[i] = threads[i].get_result()
            rcg_dict = json.loads(results[i])
            if rcg_dict.get('code') == '10105':
                print('IP错误, 请把下面的IP添加至讯飞云IP白名单并等待两分钟再试!!')
                print(rcg_dict.get('desc').strip('illegal access|illegal client_ip: '))  # no need to use replace here
                print()
                raise Exception('RCG IP Error')
        logging.debug('Multi-threads rcg results: %s' % results)
        return results


def rcg_and_save(wave_file, rcg_fp, segments=0, timeout=600, x_appid=None, api_key=None, stop_on_failure=True):
    rcg_result = rcg(wave_file, segments=segments, timeout=timeout, x_appid=x_appid, api_key=api_key)
    if isinstance(rcg_result, str):
        rcg_dict = json.loads(rcg_result)
        logging.debug("Recognition: %s" % rcg_dict.get('desc'))
        if rcg_dict.get('code') == '0':
            with open(rcg_fp, 'w') as f:
                f.write(rcg_result)
        else:
            if stop_on_failure:
                raise Exception('rcg failure: %s - %s' % (wave_file, rcg_dict.get('code')))
            else:
                logging.info('rcg failure: %s - %s' % (wave_file, rcg_dict.get('code')))
    elif isinstance(rcg_result, dict):
        rcgs_dict = {}
        rcgs_status = {}
        data_lst = []
        for i in range(len(rcg_result)):
            if rcg_result[i] is not None:
                rcgs_dict[i] = json.loads(rcg_result[i])
                rcgs_status[i] = rcgs_dict[i]['desc']
                if rcgs_dict[i].get('code') == '0':
                    data_lst.append(rcgs_dict[i].get('data'))
                else:
                    if stop_on_failure:
                        raise Exception('rcg failure: %s SEG %d - %s' % (wave_file, i, rcgs_dict[i].get('code')))
                    else:
                        logging.info('rcg failure: %s SEG %d - %s' % (wave_file, i, rcgs_dict[i].get('code')))
            else:
                data_lst.append('')
        logging.debug('Multi segments rcg result: %s' % rcgs_status)

        if rcg_result[0] is None:
            rcgs_dict[0] = {'code': '0', 'data': '', 'desc': 'None'}

        if segments == 0:  # 自动分段的结果自动合并
            rcgs_dict[0]['data'] = ''.join(data_lst)
        else:  # 手动指定分段的保存各次识别结果为列表
            rcgs_dict[0]['data'] = data_lst
        with open(rcg_fp, 'w') as ff:
            ff.write(json.dumps(rcgs_dict[0], ensure_ascii=False))  # dump as utf-8
    if not os.path.exists(rcg_fp):
        with open(rcg_fp, 'w') as f:
            rcgs_dict = {'code': '0', 'data': '', 'desc': 'None'}
            f.write(json.dumps(rcgs_dict, ensure_ascii=False))  # dump as utf-8


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:\t%(message)s')

    # result = rcg(config.WAV_FILE_PATH, segments=1, timeout=100)
    # print(isinstance(result, str))
    # print(isinstance(result, dict))

    rcg_fp = 'temp_dylanchu/rcgtest.json'
    # rcg_and_save(config.WAV_FILE_PATH, rcg_fp, segments=3, timeout=1, stop_on_failure=True)
    rcg(config.WAV_FILE_PATH, timeout=10, segments=3)

    with open(rcg_fp, 'r') as f:
        print(f.read())
