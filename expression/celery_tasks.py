#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-8-18

import os
import logging
import traceback
import baidu_bos
import config
import db
import analysis_features
import analysis_scores

from celery import Celery
from kombu import Queue, Exchange

app = Celery('tasks', broker=config.Celery_broker, backend=config.Celery_backend)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:\t%(message)s')

# 配置队列
CELERY_QUEUES = (
    # Queue('for_q_type3', Exchange('for_q_type3'), routing_key='for_q_type3', consumer_arguments={'x-priority': 10}),
    # Queue('for_q_type12', Exchange('for_q_type12'), routing_key='for_q_type12', consumer_arguments={'x-priority': 1}),
    Queue('for_q_type3', Exchange('for_q_type3'), routing_key='for_q_type3', queue_arguments={'x-max-priority': 100}),
    Queue('for_q_type12', Exchange('for_q_type12'), routing_key='for_q_type12', queue_arguments={'x-max-priority': 2}),
    Queue('default', Exchange('default'), routing_key='default', queue_arguments={'x-max-priority': 1}),
)  # consumer_arguments={'x-priority': 5}   数字越大，优先级越高

BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 86400}

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
CELERY_ROUTES = {
    # -- HIGH PRIORITY QUEUE -- #
    'app.tasks.analysis_main_3': {'queue': 'for_q_type3'},
    # -- LOW PRIORITY QUEUE -- #
    'app.tasks.analysis_main_12': {'queue': 'for_q_type12'},
    'app.tasks.analysis_main': {'queue': 'default'},
}


def analysis_main(current_id, q_num):
    # current_id = "5bcde8f30b9e037b1f67ba4e"
    # q_num = "2"
    logging.info("current_id: %s, q_num: %s" % (current_id, q_num))

    mongo = db.Mongo()

    feature = {}
    score = 0
    status = 'finished'
    tr = None
    # feature = get_feature(wf, q)
    # score = get_score(q, feature)

    q_info = mongo.get_question_info(current_id, q_num)
    wf, q = mongo.get_wave_path_and_question(q_info)

    try:
        # get api accounts
        # evl_account = mongo.get_evl_account()
        # rcg_account = mongo.get_rcg_account()
        # baidu_account = mongo.get_baidu_account()
        # config.XF_EVL_APP_ID = evl_account['appid']
        # config.XF_EVL_API_KEY = evl_account['key']
        # config.XF_RCG_APP_ID = rcg_account['appid']
        # config.XF_RCG_API_KEY = rcg_account['key']
        # config.BD_NLP_APP_ID = baidu_account['appid']
        # config.BD_NLP_API_KEY = baidu_account['api_key']
        # config.BD_NLP_SECRET_KEY = baidu_account['secret_key']
        # logging.info('using EVL account: %s' % evl_account)
        # logging.info('using RCG account: %s' % rcg_account)
        # logging.info('using BAIDU account: %s' % baidu_account)

        Q_type = q['q_type']
        file_location = q.get('file_location', 'local')
        path = baidu_bos.get_file(q_info['wav_temp_url'], location=file_location)

        if Q_type == 1:
            feature = analysis_features.analysis1(path, q['text'], timeout=30)
            score = analysis_scores.score1(feature)
            # 默认百度识别，若用讯飞识别，需注明参数：
            # feature = analysis_features.analysis1(path, q['text'], timeout=30, rcg_interface='xunfei')
            # score = analysis_scores.score1(feature,rcg_interface='xunfei')
        elif Q_type == 2:
            feature = analysis_features.analysis2(path, q['wordbase'], timeout=30)
            score = analysis_scores.score2(feature)
        elif Q_type == 3:
            feature = analysis_features.analysis3(path, q['wordbase'], timeout=30)
            score = analysis_scores.score3(feature)
        else:
            logging.error('Invalid question type: %s' % Q_type)

        status = 'finished'
        tr = None
    except Exception as e:
        tr = traceback.format_exc()
        print(tr)
        logging.error('error happened during process task: %s' % e)
        status = 'error'

    logging.info('Score: %s' % score)
    mongo.save_result(current_id, q_num, q_info, feature, score, status=status, stack=tr)
    os.system('rm %s' % q_info['wav_temp_url'])
    os.system('rmdir %s > /dev/null 2>&1' % os.path.dirname(q_info['wav_temp_url']))
    return status


@app.task
def analysis_main_12(current_id, q_num):
    return analysis_main(current_id, q_num)


@app.task
def analysis_main_3(current_id, q_num):
    return analysis_main(current_id, q_num)
