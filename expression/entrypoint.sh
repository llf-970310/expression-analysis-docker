#!/bin/sh

echo executing entrypoint.sh ...
# celery worker -A celery_tasks.app -n worker_Qtype3 -Q q_type3 --loglevel=info --concurrency=30 &
# celery worker -A celery_tasks.app -n worker_Qtype12 -Q q_type12 --loglevel=info --concurrency=30 &
# celery worker -A celery_tasks.app -n worker_Type123 -Q q_type3,q_type12 --loglevel=info --concurrency=10 &
# celery multi start 2 -P gevent -A celery_tasks.app -n worker_Type3@%h -Q q_type3 -l info -c:1-2 15 &
# celery multi start 2 -P gevent -A celery_tasks.app -n worker_Type12@%h -Q q_type12 -l info -c:1-2 15 &
celery worker -P gevent -A celery_tasks.app -n %h_Qt-Pre_p1 -Q q_pre_test -l info -c 15 &
celery worker -P gevent -A celery_tasks.app -n %h_Qt-Pre_p2 -Q q_pre_test -l info -c 15 &
celery worker -P gevent -A celery_tasks.app -n %h_Qt-12_p1 -Q q_type12 -l info -c 30 &
celery worker -P gevent -A celery_tasks.app -n %h_Qt-3_p1 -Q q_type3 -l info -c 30

# celery flower -A celery_tasks.app --address=0.0.0.0 --port=50080
