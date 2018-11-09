#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 18-10-19

import datetime
import logging
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
        self.api_accounts = mdb[config.MONGODB_COLLECTION_APIS]

    def get_question_info(self, current_id, q_num):
        return self.current.find_one({"_id": ObjectId(current_id)})['questions'][q_num]

    def get_wave_path_and_question(self, question_info):  # current_id and q_num should be strings
        """ 获取： 音频文件路径 和 要分析问题的详细信息
        要使用传入的 q_num 而不使用 current表中的 current_q_num，因为 current_q_num 只是django维护的临时标记，随时会改变。
        """
        logging.debug(question_info)
        wave_path = question_info['wav_temp_url']
        question = self.questions.find_one({"_id": ObjectId(question_info['q_id'])})
        logging.debug('wave_path: %s, question: %s' % (wave_path, question))
        return wave_path, question

    def save_result(self, current_id, q_num, question_info, feature=None, score=None, status='finished', stack=None):
        """ 根据给定的current_id和q_num，
        设置当前题目status为finished，保存分析结果feature{}，保存该题score，保存分析结束时间analysis_end_time
        若当前题目处理出错，保存堆栈信息
        """
        if status == 'finished':
            question_info['feature'] = feature
            question_info['score'] = score
        else:
            question_info['stack'] = stack
        question_info['status'] = status
        question_info['analysis_end_time'] = datetime.datetime.utcnow()
        self.current.update_one({'_id': ObjectId(current_id)}, {'$set': {'questions.%s' % q_num: dict(question_info)}},
                                True)  # 参数分别是：条件，更新内容，不存在时是否插入

    # def test_insert_data(self):
    #     with open('/tmp/current.json', 'r') as f:
    #         data = json.loads(f.read())
    #     self.current.insert_one(data)

    # def test_find(self):
    #     current_item = self.current.find_one({"_id": ObjectId("5bcdc98e0b9e0365ce135a68")})  # format right! found!
    #     current_item = self.current.find_one({"_id": "5bcdc98e0b9e0365ce135a68"})  # format wrong! not found!
    #     logging.info(current_item)

    def get_evl_account(self):
        """
        :return: dict like {'appid': 'xxx', 'key': 'xxx', 'used_times': 6}
        """
        evl_accounts = self.api_accounts.find_one({"type": "xf_evl"})
        all_accounts = evl_accounts['accounts']
        all_accounts = sorted(all_accounts, key=lambda a: a['used_times'], reverse=False)
        all_accounts[0]['used_times'] += 1
        self.api_accounts.update_one({'_id': evl_accounts['_id']}, {'$set': {'accounts': list(all_accounts)}}, False)
        return all_accounts[0]

    def get_rcg_account(self):
        """
        :return: dict like {'appid': 'xxx', 'key': 'xxx', 'used_times': 6}
        """
        rcg_accounts = self.api_accounts.find_one({"type": "xf_rcg"})
        all_accounts = rcg_accounts['accounts']
        all_accounts = sorted(all_accounts, key=lambda a: a['used_times'], reverse=False)
        all_accounts[0]['used_times'] += 1
        self.api_accounts.update_one({'_id': rcg_accounts['_id']}, {'$set': {'accounts': list(all_accounts)}}, False)
        return all_accounts[0]

    def get_baidu_account(self):
        """
        :return: dict like {'appid': 'xxx', 'api_key': 'xxx', 'secret_key': 'xxx', 'used_times': 6}
        """
        baidu_accounts = self.api_accounts.find_one({"type": "baidu"})
        all_accounts = baidu_accounts['accounts']
        all_accounts = sorted(all_accounts, key=lambda a: a['used_times'], reverse=False)
        all_accounts[0]['used_times'] += 1
        self.api_accounts.update_one({'_id': baidu_accounts['_id']}, {'$set': {'accounts': list(all_accounts)}}, False)
        return all_accounts[0]


if __name__ == '__main__':
    current_id = "5bcde8f30b9e037b1f67ba4e"
    q_num = "2"

    db = Mongo()
    q_info = db.get_question_info(current_id, q_num)
    wf, q = db.get_wave_path_and_question(q_info)
    feature = {}
    score = {"main": 60, "detail": 80}
    db.save_result(current_id, q_num, q_info, feature, score)

    # m = Mongo()
    # print(m.get_evl_account())
    # print(m.get_rcg_account())
    # print(m.get_baidu_account())
