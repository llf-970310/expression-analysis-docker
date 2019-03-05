#!/bin/sh

echo executing entrypoint.sh ...
celery worker -A celery_tasks.app -n worker_Qtype3 -Q for_q_type3 --loglevel=info --concurrency=10 &
celery worker -A celery_tasks.app -n worker_Qtype12 -Q for_q_type12 --loglevel=info --concurrency=10 &
#celery worker -A celery_tasks.app -n worker_Qtype123 -Q for_q_type3,for_q_type12 --loglevel=info --concurrency=10 &
celery flower -A celery_tasks.app --address=0.0.0.0 --port=50080