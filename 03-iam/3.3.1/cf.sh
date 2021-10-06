#!/usr/bin/env bash

aws cloudformation $1-stack --stack-name kpu-lab-03 --template-body file://iam.yaml --capabilities CAPABILITY_NAMED_IAM | jq .
