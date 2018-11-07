#!/bin/bash

cd `dirname $0`
pwd
docker images -a|grep exp-analysis|grep days|grep -v latest|awk '{print $3}'|xargs docker rmi
tags=$(date +%Y%m%d-%H%M)
docker build ./ -t exp-analysis:$tags
docker tag exp-analysis:$tags exp-analysis:latest
