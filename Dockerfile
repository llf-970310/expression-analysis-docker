FROM python:3.6.7-alpine3.7
MAINTAINER dylanchu <chdy.uuid@gmail.com>

RUN apk add --no-cache tzdata && \
    cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    rm /usr/share/zoneinfo/ -rf && \
    mkdir -p /usr/share/zoneinfo/Asia/ && \
    cp -f /etc/localtime /usr/share/zoneinfo/Asia/Shanghai

RUN apk add --no-cache make cmake gcc g++ gfortran && \
    pip install numpy baidu-aip webrtcvad python-levenshtein pymongo pypinyin zhon && \
    apk del make cmake gcc g++ gfortran && \
    rm -rf /root/.cache/pip

RUN pip install redis 'celery[redis]'  && \
    pip install --upgrade https://github.com/celery/celery/tarball/master && \
    pip install flower && \
    rm -rf /root/.cache/pip

EXPOSE 50080

COPY expression /expression
WORKDIR expression
ENTRYPOINT ["celery", "worker", "-A", "celery_tasks.app"]
