#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-10-19

import datetime
import json
import pymongo
import config
from bson.objectid import ObjectId


class Mongo(object):
    def __init__(self):
        host = config.MONGODB_HOST
        port = config.MONGODB_PORT
        password = config.MONGODB_PASSWORD
        username = config.MONGODB_USERNAME
        authSource = config.MONGODB_DBNAME
        authMechanism = config.MONGODB_AUTH_MECHANISM

        if config.MONGODB_NEED_AUTH:
            client = pymongo.MongoClient(host=host, port=port, username=username, password=password,
                                         authSource=authSource, authMechanism=authMechanism)  # 创建数据库连接
        else:
            client = pymongo.MongoClient(host=host, port=port)  # 创建数据库连接
        mdb = client[config.MONGODB_DBNAME]  # db
        self.current = mdb[config.MONGODB_COLLECTION_CURRENT]  # collection
        self.questions = mdb[config.MONGODB_COLLECTION_QUESTIONS]

    def get_question_info(self, current_id, q_num):
        return self.current.find_one({"_id": ObjectId(current_id)})['questions'][q_num]

    def get_wave_path_and_question(self, question_info, q_num):  # current_id and q_num should be strings
        """ 获取： 音频文件路径 和 要分析问题的详细信息
        要使用传入的 q_num 而不使用 current表中的 current_q_num，因为 current_q_num 只是django维护的临时标记，随时会改变。
        """
        print(question_info)
        wave_path = question_info['wav_temp_url']
        question = self.questions.find_one({"_id": ObjectId(question_info['q_id'])})
        print(wave_path, question)
        return wave_path, question

    def save_result(self, current_id, q_num, question_info, feature, score):
        """ 根据给定的current_id和q_num，
        设置当前题目status为finished，保存分析结果feature{}，保存该题score，保存分析结束时间analysis_end_time
        """
        question_info['status'] = 'finished'
        question_info['feature'] = feature
        question_info['score'] = score
        question_info['analysis_end_time'] = datetime.datetime.utcnow().__str__()
        self.current.update_one({'_id': ObjectId(current_id)}, {'$set': {'questions.%s' % q_num: dict(question_info)}}, True)  # 参数分别是：条件，更新内容，不存在时是否插入

    # def test_insert_data(self):
    #     with open('/tmp/current.json', 'r') as f:
    #         data = json.loads(f.read())
    #     self.current.insert_one(data)

    # def test_find(self):
    #     current_item = self.current.find_one({"_id": ObjectId("5bcdc98e0b9e0365ce135a68")})  # format right! found!
    #     current_item = self.current.find_one({"_id": "5bcdc98e0b9e0365ce135a68"})  # format wrong! not found!
    #     print(current_item)


if __name__ == '__main__':
    current_id = "5bcde8f30b9e037b1f67ba4e"
    q_num = "2"

    db = Mongo()
    q_info = db.get_question_info(current_id, q_num)
    wf, q = db.get_wave_path_and_question(q_info, q_num)

    # feature, score = analysis(wf, q)
    feature = {}
    score = 60

    db.save_result(current_id, q_num, q_info, feature, score)
