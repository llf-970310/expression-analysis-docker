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
import model_test.db as db

if __name__ == '__main__':
    time0, i, j = time.time(), 1, 1
    mongo = db.Mongo()
    current = mongo.get_currents()
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
                continue
            if question.get('q_type') == 2:
                wave_file = os.path.join('/expression', question.get('wav_upload_url'))
                rcg_text = question.get('feature').get('rcg_text')
                wordbase = mongo.get_question_wordbase(question_id=question.get('q_id'))
                if os.path.exists(wave_file) and os.path.isfile(wave_file):
                    analysis_result['features'] = analysis_features.analysis2(wave_file, wordbase, rcg_txt=rcg_text)
                    analysis_result['score_main'], analysis_result['score_detail'] = analysis_scores.score2(
                        analysis_result['features']).values()
                    mongo.update_or_save_analysis(analysis_result)
                    time1 = time.time()
                    print('第%d个考试第%d道题录入完成,用时:%s秒' % (i, j, str(round(time1 - time0, 2))))
                    time0 = time1
                j += 1
            if question.get('q_type') == 3:
                continue
        i += 1
    pass
