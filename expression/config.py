#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-7-17

# XUNFEI API interface
XF_RCG_URL = 'https://api.xfyun.cn/v1/service/v1/iat'
XF_EVL_URL = 'https://api.xfyun.cn/v1/service/v1/ise'

XF_EVL_CATEGORY = "read_chapter"
# rcg_param
XF_RCG_ENGINE_TYPE = "sms8k"


# -------- ACCOUNTS -------- :just default accounts, overwritten in main.py
XF_EVL_APP_ID = '5b482315'  # Ordinary account
XF_EVL_API_KEY = 'd5eabc8c4a8ea2edb03f8e486d7076b3'
XF_RCG_APP_ID = '5b482315'
XF_RCG_API_KEY = '33d2e52fe4bdddae35e09026f2167867'
BAIDU_APP_ID = '11624605'
BAIDU_API_KEY = 'Fe0cUsrl9N5zmjhmkSoE0mzL'
BAIDU_SECRET_KEY = 'cbz66d97eOwKLnvYkzhgDEoSqgMuciWO'
# --------------------------


# # jieba分词用户词典
# JIEBA_USER_DICT = "text_files/jieba_userdict.txt"


# -------- MongoDB --------
# MONGODB_HOST = '127.0.0.1'
MONGODB_HOST = '172.17.0.1'  # docker0
# MONGODB_HOST = '47.98.174.59'
MONGODB_PORT = 27017  # 默认27017
# {
# MONGODB_NEED_AUTH = True
MONGODB_NEED_AUTH = False
MONGODB_USERNAME = 'iselab'
MONGODB_PASSWORD = 'iselab###nju.cn'
MONGODB_AUTH_MECHANISM = 'SCRAM-SHA-1'
# }
MONGODB_DBNAME = 'expression'
MONGODB_COLLECTION_CURRENT = 'current'
MONGODB_COLLECTION_QUESTIONS = 'questions'
MONGODB_COLLECTION_APIS = 'api_accounts'
# -------------------------


# -------------- UAAM CONFIG --------------
INTERVAL_TIME_THRESHOLD1 = 0.7  # 第一种题型的间隔时间阈值
INTERVAL_TIME_THRESHOLD2 = 2.0  # 第二中题型的间隔时间阈值
INTERVAL_TIME_THRESHOLD3 = 2.0  # 第三种题型的间隔时间阈值
MAIN_IDEA_WORD_COUNT = 30  # 计算主旨关键词是否在前面说到时所用的字数
