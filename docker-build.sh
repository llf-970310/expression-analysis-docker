#!/bin/bash

cd `dirname $0`
pwd
tags=$(date +%Y%m%d-%H%M)
docker build ./ -t exp-analysis:$tags
docker tag exp-analysis:$tags exp-analysis:latest
