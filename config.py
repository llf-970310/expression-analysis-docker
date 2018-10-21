#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-7-17

# XUNFEI API interface
XF_RCG_URL = 'https://api.xfyun.cn/v1/service/v1/iat'
XF_EVL_URL = 'https://api.xfyun.cn/v1/service/v1/ise'

# Professional account (2 weeks till 2018-08-17)
# XF_APP_ID = '5b481e03'
# XF_RCG_API_KEY = '2727307781775b887e7323e8428223cb'
# XF_EVL_API_KEY = 'ac595ef62ad106b4c727a929aeda4a33'

# Ordinary account
# XF_APP_ID = '5b48203c'
# XF_RCG_API_KEY = '4698df1be642a83e2c8614ed594c926'
# XF_EVL_API_KEY = 'cf739d160b9fdf63c04e977bf6daef60'
XF_APP_ID = '5b482315'
XF_RCG_API_KEY = '33d2e52fe4bdddae35e09026f2167867'
XF_EVL_API_KEY = 'd5eabc8c4a8ea2edb03f8e486d7076b3'


XF_EVL_CATEGORY = "read_chapter"
# rcg_param
XF_RCG_ENGINE_TYPE = "sms8k"

# -------------- FILE PATH CONFIG --------------
# 音频文件
WAV_FILE_PATH = "audio/Samples2/1/1.wav"
# WAV_FILE_PATH = "audio/Professional2/8/1.wav"
# WAV_FILE_PATH = "temp_dylanchu/1.wav"

# 文本朗读题
# std text: 180 bytes at max, or error10109 will be raised
STD_TEXT_FILE_PATH = "text_files/Papers/朗读题.txt"
RCG_JSON_FILE_PATH = "text_files/Samples2/rcg_1_1.json"
EVL_JSON_FILE_PATH = "text_files/Samples2/evl_1_1.json"
# RCG_JSON_FILE_PATH = "text_files/Professional2/rcg_8_1.json"
# EVL_JSON_FILE_PATH = "text_files/Professional2/evl_8_1.json"

# 计算cfc(清晰度，无效表达，完成度)应使用识别结果(rcg_xxx.json)而非评测结果，使用评测结果可能过于宽松
#
# # 主旨题
# SUMMARY_ORIGINAL_FILE = "text_files/Papers/主旨题1.txt"
# SUMMARY_STD_ANSWER_FILE = "text_files/Papers/主旨题1_std_answer.txt"
# # 观点表述题
# OPINION_STATEMENT_FILE = "text_files/demo/观点表述题_回答.txt"
# # jieba分词用户词典
# JIEBA_USER_DICT = "text_files/jieba_userdict.txt"

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017  # 默认27017
MONGODB_DBNAME = 'Tenwhy'
MONGODB_DOCNAME = 'TenwhyQAs'

