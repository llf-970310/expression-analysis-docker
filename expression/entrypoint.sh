#!/bin/sh

this_ip=` ifconfig -a|grep inet|awk '{print $2}'|tr -d "addr:"|grep 192.168|sed "s/\./-/g"`

echo executing entrypoint.sh ...
# celery worker -A celery_tasks.app -n worker_Qtype3 -Q q_type3 --loglevel=info --concurrency=30 &
# celery worker -A celery_tasks.app -n worker_Qtype12 -Q q_type12 --loglevel=info --concurrency=30 &
# celery worker -A celery_tasks.app -n worker_Type123 -Q q_type3,q_type12 --loglevel=info --concurrency=10 &
# celery multi start 2 -P gevent -A celery_tasks.app -n worker_Type3@%h -Q q_type3 -l info -c:1-2 15 &
# celery multi start 2 -P gevent -A celery_tasks.app -n worker_Type12@%h -Q q_type12 -l info -c:1-2 15 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-Pre_p1" -Q q_pre_test -l info -c 20 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-12_p1" -Q q_type12 -l info -c 12 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-12_p2" -Q q_type12 -l info -c 13 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p1" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p2" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p3" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p4" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p5" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p6" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p7" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p8" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p9" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p10" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p11" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p12" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p13" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p14" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p15" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p16" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p17" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p18" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p19" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p20" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p21" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p22" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p23" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p24" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p25" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p26" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p27" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p28" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p29" -Q q_type3 -l info -c 1 &
celery worker -P gevent -A celery_tasks.app -n $this_ip"-Qt-3_p30" -Q q_type3 -l info -c 1

# celery flower -A celery_tasks.app --address=0.0.0.0 --port=50080
