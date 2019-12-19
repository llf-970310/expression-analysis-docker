#!/usr/bin/env python3
# coding: utf-8
#
# Created by dylanchu on 2019/12/20

from io import BytesIO
from subprocess import Popen, PIPE


def m4a2wav_bytes_io(bytes_io_file):
    bytes_io_file.seek(0)
    content = bytes_io_file.getvalue()
    cmd = ['ffmpeg', '-n', '-i', 'pipe:', '-acodec', 'pcm_s16le', '-f', 'wav', '-ac', '1', '-ar', '8000', 'pipe:']
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=-1)
    out, _ = p.communicate(input=content)
    p.stdin.close()
    return BytesIO(out) if out.startswith(b'RIFF\xff\xff\xff') else None


# if __name__ == '__main__':
#     file = '8-1576685164r111.m4a'
#     with open(file, 'rb') as f:
#         data = BytesIO(f.read())
#     print(type(m4a2wav_bytes_io(data)))
