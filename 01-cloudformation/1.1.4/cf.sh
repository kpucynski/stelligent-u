#!/usr/bin/env bash

REGION="${2:-us-east-2}"

aws cloudformation $1-stack --stack-name kpu-lab-01 --template-body file://s3.yaml --parameters file://s3.json --region ${REGION}
