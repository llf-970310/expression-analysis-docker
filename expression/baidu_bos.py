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

# configurations
access_key_id = config.BD_BOS_AK
secret_access_key = config.BD_BOS_SK
bos_host = config.BD_BOS_HOST
bucket_name = config.BD_BOS_BUCKET


logger = logging.getLogger("baidubce.http.bce_http_client")
logger.setLevel(logging.DEBUG)

bos_config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key), endpoint=bos_host)
bos_client = BosClient(bos_config)

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

content = bos_client.get_object_as_string(bucket_name=bucket_name, key='/audio/batchtest/1.wav')
print(type(content))
print(content)

audio = io.BytesIO(content)  # this would auto seek(0)
import wave

with wave.open(audio, 'rb') as f:
    print(f.getparams())
