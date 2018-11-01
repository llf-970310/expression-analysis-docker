#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-8-18
import os

import logging
import sys

import traceback

import config
import db
import analysis_features
import analysis_scores


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:\t%(message)s')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise Exception('arguments too less')

    current_id = sys.argv[1]
    q_num = sys.argv[2]
    # current_id = "5bcde8f30b9e037b1f67ba4e"
    # q_num = "2"
    logging.info("current_id: %s, q_num: %s" % (current_id, q_num))

    mongo = db.Mongo()

    features = dict()
    feature = {}
    score = 0
    status = 'finished'
    # feature = get_feature(wf, q)
    # score = get_score(q, feature)

    q_info = mongo.get_question_info(current_id, q_num)
    wf, q = mongo.get_wave_path_and_question(q_info)

    tries = 0
    while tries <= 3:
        try:
            # get api accounts
            evl_account = mongo.get_evl_account()
            rcg_account = mongo.get_rcg_account()
            baidu_account = mongo.get_baidu_account()
            config.XF_EVL_APP_ID = evl_account['appid']
            config.XF_EVL_API_KEY = evl_account['key']
            config.XF_RCG_APP_ID = rcg_account['appid']
            config.XF_RCG_API_KEY = rcg_account['key']
            config.BAIDU_APP_ID = baidu_account['appid']
            config.BAIDU_API_KEY = baidu_account['api_key']
            config.BAIDU_SECRET_KEY = baidu_account['secret_key']
            logging.info('using EVL account: %s' % evl_account)
            logging.info('using RCG account: %s' % rcg_account)
            logging.info('using BAIDU account: %s' % baidu_account)

            Q_type = q['q_type']
            if Q_type == 1:
                feature = analysis_features.analysis1(q_info['wav_temp_url'], q['text'], timeout=30)
                score = analysis_scores.score1(feature)
            elif Q_type == 2:
                feature = analysis_features.analysis2(q_info['wav_temp_url'], q['wordbase'], timeout=30)
                score = analysis_scores.score2(feature)
            elif Q_type == 3:
                feature = analysis_features.analysis3(q_info['wav_temp_url'], q['wordbase'], timeout=30)
                score = analysis_scores.score3(feature)
            else:
                logging.error('Invalid question type: %s' % Q_type)
            tries = 9999
            break
        except Exception as e:
            traceback.print_exc()
            logging.error('on retry %s: %s' % (tries, e))
            status = e.__str__()
            tries += 1

    logging.info('Score: %s' % score)
    mongo.save_result(current_id, q_num, q_info, feature, score, status=status)
    os.system('rm %s' % q_info['wav_temp_url'])
    os.system('rmdir %s > /dev/null 2>&1' % os.path.dirname(q_info['wav_temp_url']))
