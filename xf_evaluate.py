#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-7-13
import logging
import os
import socket
import urllib.parse
import urllib.request
import time
import json
import hashlib
import base64

import config
import utils


def evl(filename, std_text, timeout=600):
    # text: 180bytes at max, or error10109 will be raised
    with open(filename, 'rb') as f:   # 以二进制格式只读打开文件读取，bytes
        file_content = f.read()
    base64_audio = base64.b64encode(file_content)  # 参数是bytes类型，返回也是bytes类型
    body = urllib.parse.urlencode({'audio': base64_audio, 'text': std_text})

    url = config.XF_EVL_URL
    x_appid = config.XF_APP_ID
    api_key = config.XF_EVL_API_KEY
    # param = {"aue": "raw", "result_level": "complete", "language": "cn", "category": config.XF_EVL_CATEGORY, "plev": "0"}

    param = {"aue": "raw", "result_level": "complete", "language": "cn",
             "category": "read_chapter", "plev": "0"}

    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = int(int(round(time.time() * 1000)) / 1000)

    # print(x_param)  # bytes
    x_checksum_content = api_key + str(x_time) + str(x_param, 'utf-8')
    x_checksum = hashlib.md5(x_checksum_content.encode('utf-8')).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}

    req = urllib.request.Request(url=url, data=body.encode('utf-8'), headers=x_header, method='POST')
    result = urllib.request.urlopen(req, timeout=timeout)
    result = result.read().decode('utf-8')
    rcg_dict = json.loads(result)
    if rcg_dict.get('code') == '10105':
        print('IP错误, 请把下面的IP添加至讯飞云IP白名单并等待两分钟再试!!')
        print(rcg_dict.get('desc').strip('illegal access|illegal iperr ip is'))  # no need to use replace here
        print()
        raise Exception('EVL IP Error')
    return result


def evl_and_save(wave_file, std_txt_file, evl_fp, framerate=16000, stop_on_failure=True):
    if framerate == 8000 or framerate == "8000" or framerate == "8k" or framerate == "8K":
        tmp_wav_path = "/tmp/evl_tmp_16000.wav"
        utils.wav_8kto16k(wave_file, tmp_wav_path)
        wave_file = tmp_wav_path
    with open(std_txt_file, 'rb') as f:
        text = f.read()
    result = evl(wave_file, text)
    tmp_evl_dict = json.loads(result)
    logging.debug("Evaluation: %s" % tmp_evl_dict.get('desc'))
    if tmp_evl_dict['code'] == '0':
        with open(evl_fp, 'w') as f:
            f.write(result)
    else:
        print(result)
        if stop_on_failure:
            raise Exception("evl error while processing %s: code %s, desc - %s"
                            % (wave_file, tmp_evl_dict.get('code'), tmp_evl_dict.get('desc')))
        else:
            logging.error("evl error while processing %s: code %s, desc - %s"
                          % (wave_file, tmp_evl_dict.get('code'), tmp_evl_dict.get('desc')))


if __name__ == '__main__':
    # evl_and_save(config.WAV_FILE_PATH, config.STD_TEXT_FILE_PATH, config.EVL_JSON_FILE_PATH, framerate=8000)
    evl(config.WAV_FILE_PATH, config.STD_TEXT_FILE_PATH)

    # with open(config.EVL_JSON_FILE_PATH, 'r') as f:
    #     print(f.read())
