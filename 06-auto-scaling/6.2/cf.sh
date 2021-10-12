#!/usr/bin/env bash

aws cloudformation $1-stack --stack-name kpu-lab-06 --template-body file://ec2.yaml --capabilities CAPABILITY_IAM | jq .
