#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 19-1-31

import logging
import os
import threading
import json
import wave
from math import ceil
import io
import utils
import config
from aip import AipSpeech

aip_speech = AipSpeech(config.BD_RCG_APP_ID, config.BD_RCG_API_KEY, config.BD_RCG_SECRET_KEY)


class RcgCore(threading.Thread):
    def __init__(self, wav_file, timeout=600, bd_appid=None, bd_api_key=None, bd_secret_key=None):
        threading.Thread.__init__(self)
        self.wav_file = wav_file
        self.result = None
        if bd_appid and bd_api_key and bd_secret_key:
            self.aip_speech = AipSpeech(config.BD_RCG_APP_ID, config.BD_RCG_API_KEY, config.BD_RCG_SECRET_KEY)
        else:
            self.aip_speech = aip_speech
        self.aip_speech.setConnectionTimeoutInMillis(timeout * 1000)
        self.aip_speech.setSocketTimeoutInMillis(timeout * 1000)

    def run(self):
        file_content = utils.read(self.wav_file, 'rb')
        # print(len(file_content))
        try:
            # 注明pcm而非wav，免去再次百度转换（可在一定情况下避免err3301：音质问题）
            rst = self.aip_speech.asr(file_content, 'pcm', 8000,
                                      {'dev_pid': '1537', 'lan': 'zh'})  # 1536是str，不是数字（报验证错误）
            """
           dev_pid	语言	                     模型      是否有标点	    备注
            1536	普通话(支持简单的英文识别)	搜索模型	    无标点	支持自定义词库
            1537	普通话(纯中文识别)        输入法模型	有标点	不支持自定义词库
            1737	英语		                            无标点	不支持自定义词库
            1637	粤语		                            有标点	不支持自定义词库
            1837	四川话		                        有标点	不支持自定义词库
            1936	普通话远场	            远场模型	    有标点	不支持 
            """
            if rst['err_no'] != 0:
                logging.error('识别错误：%s' % rst.get('err_msg'))
                logging.error(rst)
                raise Exception('Recognition failed!')
            self.result = rst['result'][0]  # rcg text
            logging.debug("Recognition: %s" % self.result)
        except Exception as e:
            logging.warning(e)

    def get_result(self):
        return self.result


def _rcg(wav_file, timeout=600, segments=0, bd_appid=None, bd_api_key=None, bd_secret_key=None):
    # 音频切段：
    segment_files = {}
    if isinstance(wav_file, io.BytesIO):
        wav_file.seek(0)  # seek(0) before read
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
                segment_files[i] = io.BytesIO()
                seg_data = wf.readframes(seg_length)
                with wave.open(segment_files[i], 'wb') as seg:
                    seg.setnchannels(nchannels)
                    seg.setsampwidth(sampwidth)
                    seg.setframerate(framerate)
                    seg.writeframes(seg_data)
    # 识别：
    if segments == 1:  # return is a 'str' object
        rcg_core = RcgCore(wav_file, timeout, bd_appid, bd_api_key, bd_secret_key)
        rcg_core.start()
        rcg_core.join()
        rcg_text = rcg_core.get_result()
        if rcg_text is None:
            raise Exception('No recognition results returned')
        return rcg_text
    if segments >= 2:  # return is a 'dict' object
        threads = dict()
        results = {}

        for i in range(segments):
            threads[i] = RcgCore(segment_files[i], timeout, bd_appid, bd_api_key, bd_secret_key)
            threads[i].start()

        for i in range(segments):
            threads[i].join()

        for i in range(segments):
            results[i] = threads[i].get_result()
        logging.debug('Multi-threads rcg results: %s' % results)
        return results


def rcg_and_save(wave_file, rcg_fp, segments=0, timeout=600, bd_appid=None, bd_api_key=None, bd_secret_key=None,
                 stop_on_failure=True):
    rcg_result = _rcg(wave_file, segments=segments, timeout=timeout, bd_appid=bd_appid, bd_api_key=bd_api_key,
                      bd_secret_key=bd_secret_key)
    if isinstance(rcg_result, str):
        if rcg_result is None:
            if stop_on_failure:
                raise Exception('file rcg failure: %s' % wave_file)
            else:
                logging.info('file rcg failure: %s' % wave_file)
        rcg_dict = {'code': '0', 'data': rcg_result, 'desc': 'None'}
        utils.write(rcg_fp, json.dumps(rcg_dict, ensure_ascii=False), 'w')
    elif isinstance(rcg_result, dict):
        data_lst = []
        for i in range(len(rcg_result)):
            if rcg_result[i] is None:
                if stop_on_failure:
                    raise Exception('file rcg failure: %s SEG %d' % (wave_file, i))
                else:
                    logging.info('file rcg failure: %s SEG %d' % (wave_file, i))
                data_lst.append('')
            else:
                data_lst.append(rcg_result[i])
        logging.info('Multi segments rcg result: %s' % data_lst)

        if rcg_result.get(0) is None:  # no rcg results
            raise Exception('file rcg failure: no rcg results')

        rcg_dict = {'code': '0', 'data': '', 'desc': 'None'}
        if segments == 0:  # 自动分段的结果自动合并
            rcg_dict['data'] = ''.join(data_lst)
        else:  # 手动指定分段的保存各次识别结果为列表
            rcg_dict['data'] = data_lst  # 结果列表不要转为字符串 tangdaye 11-04
        utils.write(rcg_fp, json.dumps(rcg_dict, ensure_ascii=False), 'w')  # dump as utf-8

    if isinstance(rcg_fp, str):  # ensure file is created when ignore errors
        if not os.path.exists(rcg_fp):
            rcg_dict = {'code': '0', 'data': '', 'desc': 'None'}
            utils.write(rcg_fp, json.dumps(rcg_dict, ensure_ascii=False), 'w')  # dump as utf-8


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:\t%(message)s')

    # result = rcg(config.WAV_FILE_PATH, segments=1, timeout=100)
    # rcg(config.WAV_FILE_PATH, timeout=10, segments=3)
    # print(isinstance(result, str))
    # print(isinstance(result, dict))

    wave_file_processed = io.BytesIO()
    interval_list = utils.find_and_remove_intervals('net_test.wav', wave_file_processed)

    rcg_fp = io.StringIO()
    rcg_and_save(wave_file_processed, rcg_fp, segments=3, timeout=10, stop_on_failure=True)

    print(utils.read(rcg_fp))