#!/bin/sh

echo executing entrypoint.sh ...
celery worker -A celery_tasks.app -n worker_default -Q default --loglevel=info --concurrency=5 &
celery worker -A celery_tasks.app -n worker_Qtype12 -Q for_question_type12 --loglevel=info --concurrency=12 &
celery worker -A celery_tasks.app -n worker_Qtype3 -Q for_question_type3 --loglevel=info --concurrency=8 &
celery flower -A celery_tasks.app --address=0.0.0.0 --port=50080
