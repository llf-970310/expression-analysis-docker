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
import time

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

    user_answer_info = mongo.get_user_answer_info(current_id, q_num)
    # 要使用传入的 q_num 而不使用 current表中的 current_q_num，因为 current_q_num 只是django维护的临时标记，随时会改变。

    q = mongo.get_problem(user_answer_info['q_id'])
    file_location = ''
    audio_key = ''
    path = ''
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

        file_location = user_answer_info.get('file_location', 'local')
        audio_key = user_answer_info['wav_upload_url']
        count = 0
        while path == '':
            time.sleep(2)
            path = baidu_bos.get_file(audio_key, location=file_location)
            count += 1
            if count >10:
                break

        Q_type = q['q_type']
        if path != '':
            if Q_type == 1:
                feature = analysis_features.analysis1(path, q['text'], timeout=30)
                score = analysis_scores.score1(feature)
            # 默认百度识别，若用讯飞识别，需注明参数：
            # feature = analysis_features.analysis1(path, q['text'], timeout=30, rcg_interface='xunfei')
            # score = analysis_scores.score1(feature,rcg_interface='xunfei')
            elif Q_type == 2:
                key_weights = q['weights']['key']
                detail_weights = q['weights']['detail']
                feature = analysis_features.analysis2(path, q['wordbase'], timeout=30)
                score = analysis_scores.score2(feature['key_hits'], feature['detail_hits'], key_weights, detail_weights)
            elif Q_type == 3:
                feature = analysis_features.analysis3(path, q['wordbase'], timeout=30)
                score = analysis_scores.score3(feature)
            else:
                logging.error('Invalid question type: %s' % Q_type)
            status = 'finished'
            tr = None
        else:
            status = 'error'

    except Exception as e:
        tr = traceback.format_exc()+"\naudio:"+audio_key+"\nfile_location:"+file_location+"\npath:"+path
        print(tr)
        logging.error('error happened during process task: %s' % e)
        status = 'error'

    logging.info('Score: %s' % score)
    mongo.save_result(current_id, q_num, user_answer_info, feature, score, status=status, stack=tr)
    return status


@app.task
def analysis_main_12(current_id, q_num):
    return analysis_main(current_id, q_num)


@app.task
def analysis_main_3(current_id, q_num):
    return analysis_main(current_id, q_num)


if __name__ == '__main__':
    status = analysis_main("5bea5322dd626213f79b945c", "2")
    print(status)
