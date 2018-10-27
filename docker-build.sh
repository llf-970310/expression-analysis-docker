#!/bin/bash

cd `dirname $0`
pwd
docker build ./ -t exp-analysis:$(date +%Y%m%d-%H%M)
