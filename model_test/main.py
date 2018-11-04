# -*- coding: utf-8 -*-
# Time: 18-11-4 下午2:22
# Author: tangdaye
# Desc: 测试

import json

if __name__ == '__main__':
    x = ['asddd','asss','asssss']
    y = {"data":x.__str__()}
    with open('./test.txt' ,'w') as f:
        f.write(json.dumps(y))