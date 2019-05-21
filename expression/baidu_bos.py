#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 19-3-10

import logging
from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient
import io
import config
import time

# configurations
access_key_id = config.BD_BOS_AK
secret_access_key = config.BD_BOS_SK
bos_host = config.BD_BOS_HOST
bucket_name = config.BD_BOS_BUCKET


def get_file(path, location='bos'):
    if location == 'bos' or location == 'BOS':
        logger = logging.getLogger("baidubce.http.bce_http_client")
        logger.setLevel(logging.DEBUG)
        logging.info('Getting file from Baidu BOS...')

        bos_config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),
                                            endpoint=bos_host)
        bos_client = BosClient(bos_config)
        content = bos_client.get_object_as_string(bucket_name=bucket_name, key=path)
        audio = io.BytesIO(content)  # this would auto seek(0)
        return audio
    elif location == 'local' or location == 'LOCAL':
        return '/expression/%s' % path


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s:\t%(message)s')
    print(get_file('audio/2019-05-21/5c939bb4cb08361b85b63be9/1558444193r688.wav','BOS'))  # BOS默认目录是根目录，最前有无/都可以
    # print(get_file('/audio/batchtest/1.wav'))

# response = bos_client.list_buckets()
# for bucket in response.buckets:
#     print(bucket.name)

# ret = bos_client.put_object_from_string(bucket='ise-expression-bos', key='/test.txt', data='hello world')
# print(ret)
# with open('net_test.wav', 'rb') as f:
#     data = f.read()
#
# wf = io.BytesIO(data)
# ret = bos_client.put_object_from_file(bucket=bucket_name, key='/test-BytesIO-file.wav', file_name=wf)
# print(ret)
# f2 = io.StringIO('hello world')
# ret = bos_client.put_object_from_file(bucket='ise-expression-bos', key='/test.txt', file_name=f2)
# print(ret)
# logger = logging.getLogger("baidubce.http.bce_http_client")
# logger.setLevel(logging.DEBUG)
#
# bos_config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),
#                                     endpoint=bos_host)
# bos_client = BosClient(bos_config)
# content = bos_client.get_object_as_string(bucket_name=bucket_name, key='/audio/batchtest/1.wav')
#
# print('cc' + str(type(content)))
# print(content)

# audio = io.BytesIO(content)  # this would auto seek(0)
