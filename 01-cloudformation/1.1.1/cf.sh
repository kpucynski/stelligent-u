#!/usr/bin/env bash

aws cloudformation $1-stack --stack-name kpu-lab-01 --template-body file://s3.yaml
