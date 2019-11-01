#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-7-17


# -------- RCG --------
RCG_MAX_RETRY = 3


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

BD_NLP_APP_ID = '11624605'
BD_NLP_API_KEY = 'Fe0cUsrl9N5zmjhmkSoE0mzL'
BD_NLP_SECRET_KEY = 'cbz66d97eOwKLnvYkzhgDEoSqgMuciWO'

BD_RCG_APP_ID = '15566115'
BD_RCG_API_KEY = '6KBIuABS3kMI7R657yyfyHlC'
BD_RCG_SECRET_KEY = 'kaTBEB3b9S3ySQrGbt7ZbRXWFw9Ro6wf'

BD_BOS_AK = '62d41797b866439b88a516fc4c8e28df'  # chu
BD_BOS_SK = '7b181acf3d5448e9b36e9e9eced6e3c8'
BD_BOS_HOST = 'su.bcebos.com'
BD_BOS_BUCKET = 'ise-expression-bos'
# --------------------------


# # jieba分词用户词典
# JIEBA_USER_DICT = "text_files/jieba_userdict.txt"


# -------- MongoDB --------
class MongoConfig(object):
    # 'host' = '127.0.0.1'
    # host = '172.17.0.1'  # docker0
    host = 'redis-server.expression.hosts'
    port = 27017  # 默认27017
    # {
    # auth = None
    auth = 'SCRAM-SHA-1'  # auth mechanism, set to None if auth is not needed
    user = 'iselab'
    password = 'iselab###nju.cn'
    # }
    db = 'expression'
    current = 'current'
    questions = 'questions'
    api_accounts = 'api_accounts'
    users = 'users'
    history = 'history'
    analysis = 'analysis'
    wav_test = 'wav_test'
# -------------------------


# Celery_broker = 'amqp://ise:ise_expression@localhost:5672//'
Celery_broker = 'redis://:ise_expression@redis-server.expression.hosts:6379/0'  # care firewall
# Celery_broker = 'redis://:ise_expression@172.17.0.1:6379/0'  # docker0
# Celery_broker = 'redis://localhost:6379/0'
Celery_backend = Celery_broker


# -------------- UAAM CONFIG --------------
INTERVAL_TIME_THRESHOLD1 = 0.7  # 第一种题型的间隔时间阈值
SEGMENTS_VOLUME1 = 3  # 第一种题型计算音量时分的段数
INTERVAL_TIME_THRESHOLD2 = 2.0  # 第二种题型的间隔时间阈值
SEGMENTS_RCG1 = 3  # 第二种识别时分的段数
SEGMENTS_RCG2 = 3  # 第二种识别时分的段数
SEGMENTS_VOLUME2 = 3  # 第二种题型计算音量时分的段数
INTERVAL_TIME_THRESHOLD3 = 2.0  # 第三种题型的间隔时间阈值
SEGMENTS_RCG3 = 3  # 第三种识别时分的段数
SEGMENTS_VOLUME3 = 3  # 第三种题型计算音量时分的段数
MAIN_IDEA_WORD_COUNT = 30  # 计算主旨关键词是否在前面说到时所用的字数
