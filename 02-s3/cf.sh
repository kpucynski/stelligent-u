#!/usr/bin/env bash

aws cloudformation $1-stack --stack-name kpu-lab-02 --template-body file://s3.yaml | jq .
