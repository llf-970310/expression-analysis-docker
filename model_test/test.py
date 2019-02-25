# -*- coding: utf-8 -*-
# Time       : 2018/12/4 10:00 AM
# Author     : tangdaye
# Description: todo
import os
import sys
import time

dir_name = os.path.realpath(__file__).split('model_test')[0]
sys.path.append(dir_name)
sys.path.append(os.path.join(dir_name, 'expression'))
sys.path.append(os.path.join(dir_name, 'model_test'))
import expression.analysis_scores as analysis_scores
import expression.analysis_features as analysis_features
import expression.xf_recognise as xf_recognise
import model_test.db as db
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import spline
import time


def xunfei_rcg(path):
    time1 = time.time()
    xf_recognise.rcg_and_save(wave_file=path, rcg_fp='./result.json')
    time2 = time.time()
    print("用时：%ss" % str(time2 - time1))
    pass


def compare():
    time0, i, j = time.time(), 1, 1
    mongo = db.Mongo()
    current = mongo.get_currents()
    scores1, scores2 = [], []
    for exam in current:
        exam_id = exam.get('_id').__str__()
        user_id = exam.get('user_id')
        user = mongo.get_user(user_id)
        questions = exam.get('questions')
        for key, question in questions.items():
            analysis_result = {
                'exam_id': exam_id,
                'user': user,
                'question_id': question.get('q_id'),
            }
            if question.get('q_type') == 1:
                features = question.get('feature')
                if features and len(features) > 0:
                    xunfei_score = analysis_scores.score1(features).get('quality')
                    baidu_score = analysis_scores.score1(features, mode="baidu").get('quality')
                    if xunfei_score >= 40:
                        scores1.append(xunfei_score)
                        scores2.append(baidu_score)
                        # print('第%d个考试，讯飞分数：%s 百度分数：%s' % (i, str(round(xunfei_score, 2)), str(round(baidu_score, 2))))
            if question.get('q_type') == 2:
                continue
                # wave_file = os.path.join('/expression', question.get('wav_upload_url'))
                # rcg_text = question.get('feature').get('rcg_text')
                # wordbase = mongo.get_question_wordbase(question_id=question.get('q_id'))
                # if os.path.exists(wave_file) and os.path.isfile(wave_file):
                #     analysis_result['features'] = analysis_features.analysis2(wave_file, wordbase, rcg_txt=rcg_text)
                #     analysis_result['score_main'], analysis_result['score_detail'] = analysis_scores.score2(
                #         analysis_result['features']).values()
                #     mongo.update_or_save_analysis(analysis_result)
                #     time1 = time.time()
                #     print('第%d个考试第%d道题录入完成,用时:%s秒' % (i, j, str(round(time1 - time0, 2))))
                #     time0 = time1
                # j += 1
            if question.get('q_type') == 3:
                continue
        i += 1
    scores1.sort()
    scores2.sort()
    # scores1, scores2 = np.array(scores1), np.array(scores2)
    print('讯飞数据均值%s，标准差%s' % (str(round(np.mean(scores1), 2)), str(round(np.std(scores1), 2))))
    print('百度数据均值%s，标准差%s' % (str(round(np.mean(scores2), 2)), str(round(np.std(scores2), 2))))
    freq1, freq2 = [], []
    m, n = 0, 0
    for i in range(10):
        s, t = 0, 0
        while m < len(scores1) and 40 + (i + 1) * 6 >= scores1[m] > 40 + i * 6:
            s += 1
            m += 1
        while n < len(scores2) and 40 + (i + 1) * 6 >= scores2[n] > 40 + i * 6:
            t += 1
            n += 1
        freq1.append(s)
        freq2.append(t)
    freq1, freq2 = np.array(freq1), np.array(freq2)
    x = np.linspace(40, 100, 300)
    freq1, freq2 = spline(range(40, 100, 6), freq1, x), spline(range(40, 100, 6), freq2, x)
    plt.figure(figsize=(20, 10))
    plt.plot(x, freq1, c='red')
    plt.plot(x, freq2, c='blue')
    plt.show()


if __name__ == '__main__':
    path = '/Users/tangdaye/dataset/audio/luozhenyu/4.wav'
    xunfei_rcg(path)
