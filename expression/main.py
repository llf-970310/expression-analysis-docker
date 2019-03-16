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
import baidu_bos

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
    tr = None
    # feature = get_feature(wf, q)
    # score = get_score(q, feature)

    q_info = mongo.get_question_info(current_id, q_num)
    wf, q = mongo.get_wave_path_and_question(q_info)

    tries = 0
    while tries <= 0:
        try:
            # get api accounts
            evl_account = mongo.get_evl_account()
            rcg_account = mongo.get_rcg_account()
            baidu_account = mongo.get_baidu_account()
            config.XF_EVL_APP_ID = evl_account['appid']
            config.XF_EVL_API_KEY = evl_account['key']
            config.XF_RCG_APP_ID = rcg_account['appid']
            config.XF_RCG_API_KEY = rcg_account['key']
            config.BD_NLP_APP_ID = baidu_account['appid']
            config.BD_NLP_API_KEY = baidu_account['api_key']
            config.BD_NLP_SECRET_KEY = baidu_account['secret_key']
            logging.info('using EVL account: %s' % evl_account)
            logging.info('using RCG account: %s' % rcg_account)
            logging.info('using BAIDU account: %s' % baidu_account)

            Q_type = q['q_type']
            audio_location = q.get('location', 'local')
            # 文件路径应该由参数上传，暂时用local
            path = baidu_bos.get_file(q_info['wav_temp_url'], location=audio_location)
            if Q_type == 1:
                # 默认百度识别，如果要是用讯飞识别，注明参数，下同
                # feature = analysis_features.analysis1(path, q['text'], timeout=30,
                #                                       rcg_interface='xunfei')
                feature = analysis_features.analysis1(path, q['text'], timeout=30)
                # 默认百度识别评分，如果要用讯飞识别评分，注明参数，下同
                # score = analysis_scores.score1(feature,rcg_interface='xunfei')
                score = analysis_scores.score1(feature)
            elif Q_type == 2:
                feature = analysis_features.analysis2(path, q['wordbase'], timeout=30)
                score = analysis_scores.score2(feature)
            elif Q_type == 3:
                feature = analysis_features.analysis3(path, q['wordbase'], timeout=30)
                score = analysis_scores.score3(feature)
            else:
                logging.error('Invalid question type: %s' % Q_type)
            tries = 9999
            status = 'finished'
            tr = None
            break
        except Exception as e:
            tr = traceback.format_exc()
            print(tr)
            logging.error('on retry %s: %s' % (tries, e))
            status = 'error'
            tries += 1

    logging.info('Score: %s' % score)
    mongo.save_result(current_id, q_num, q_info, feature, score, status=status, stack=tr)
    os.system('rm %s' % q_info['wav_temp_url'])
    os.system('rmdir %s > /dev/null 2>&1' % os.path.dirname(q_info['wav_temp_url']))
