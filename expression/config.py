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

BAIDU_APP_ID = '11624605'
BAIDU_API_KEY = 'Fe0cUsrl9N5zmjhmkSoE0mzL'
BAIDU_SECRET_KEY = 'cbz66d97eOwKLnvYkzhgDEoSqgMuciWO'

# # jieba分词用户词典
# JIEBA_USER_DICT = "text_files/jieba_userdict.txt"

MONGODB_HOST = '127.0.0.1'
# MONGODB_HOST = '47.98.174.59'
MONGODB_PORT = 27017  # 默认27017
MONGODB_DBNAME = 'expression'
MONGODB_COLLECTION_CURRENT = 'current'
MONGODB_COLLECTION_QUESTIONS = 'questions'
MONGODB_COLLECTION_APIS = 'api_accounts'
# MONGODB_NEED_AUTH = True
MONGODB_NEED_AUTH = False
MONGODB_USERNAME = 'iselab'
MONGODB_PASSWORD = 'iselab###nju.cn'
MONGODB_AUTH_MECHANISM = 'SCRAM-SHA-1'

# -------------- UAAM CONFIG --------------
INTERVAL_TIME_THRESHOLD1 = 0.7  # 第一种题型的间隔时间阈值
INTERVAL_TIME_THRESHOLD2 = 2.0  # 第二中题型的间隔时间阈值
INTERVAL_TIME_THRESHOLD3 = 2.0  # 第三种题型的间隔时间阈值
MAIN_IDEA_WORD_COUNT = 30  # 计算主旨关键词是否在前面说到时所用的字数
