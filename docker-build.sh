#!/bin/bash

cd `dirname $0`
pwd
latest=`docker images -a|grep exp-analysis|grep latest|awk '{print $3}'`
docker images -a|grep exp-analysis|grep -v ${latest}|xargs docker rmi
tags=$(date +%Y%m%d-%H%M)
docker build ./ -t exp-analysis:${tags}
docker tag exp-analysis:${tags} exp-analysis:latest
