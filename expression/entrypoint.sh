#!/bin/sh

echo executing entrypoint.sh ...
# celery worker -A celery_tasks.app -n worker_Qtype3 -Q q_type3 --loglevel=info --concurrency=30 &
# celery worker -A celery_tasks.app -n worker_Qtype12 -Q q_type12 --loglevel=info --concurrency=30 &
celery worker -P gevent -A celery_tasks.app -n Qtype3_worker1@%h -Q q_type3 -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qtype3_worker2@%h -Q q_type3 -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qtype3_worker3@%h -Q q_type3 -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qtype12_worker1@%h -Q q_type12 -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qtype12_worker2@%h -Q q_type12 -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qtype12_worker3@%h -Q q_type12 -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qpre_worker1@%h -Q q_pre_test -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qpre_worker2@%h -Q q_pre_test -l info -c 10 &
celery worker -P gevent -A celery_tasks.app -n Qpre_worker3@%h -Q q_pre_test -l info -c 10
# celery multi start 2 -P gevent -A celery_tasks.app -n worker_Type3@%h -Q q_type3 -l info -c:1-2 15 &
# celery multi start 2 -P gevent -A celery_tasks.app -n worker_Type12@%h -Q q_type12 -l info -c:1-2 15 &
# celery worker -A celery_tasks.app -n worker_Type123 -Q q_type3,q_type12 --loglevel=info --concurrency=10 &

# celery flower -A celery_tasks.app --address=0.0.0.0 --port=50080
