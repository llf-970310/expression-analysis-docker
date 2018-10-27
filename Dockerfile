FROM python:3.6.7-alpine3.7
MAINTAINER dylanchu <chdy.uuid@gmail.com>

RUN apk add --no-cache tzdata && \
    cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    rm /usr/share/zoneinfo/ -rf && \
    mkdir -p /usr/share/zoneinfo/Asia/ && \
    cp -f /etc/localtime /usr/share/zoneinfo/Asia/Shanghai

RUN apk add --no-cache make cmake gcc g++ gfortran && \
    pip install numpy baidu-aip webrtcvad python-levenshtein pymongo pypinyin zhon && \
    apk del make cmake gcc g++ gfortran

COPY expression /expression
WORKDIR expression
ENTRYPOINT ["python3", "main.py"]