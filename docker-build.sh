#!/bin/bash

cd `dirname $0`
pwd
tags=$(date +%Y%m%d-%H%M)
docker build ./ -t exp-analysis:${tags}
docker tag exp-analysis:${tags} exp-analysis:latest
docker images -a|grep exp-analysis|grep -v none|awk '{print $1":"$2}'|grep -v latest|grep -v ${tags}|xargs docker rmi
