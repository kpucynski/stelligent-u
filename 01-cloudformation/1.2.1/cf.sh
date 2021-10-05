#!/usr/bin/env bash

REGION="${2:-us-east-2}"

aws cloudformation $1-stack --stack-name kpu-lab-02 --template-body file://iam.yaml --parameters file://iam.json --region ${REGION} --capabilities CAPABILITY_NAMED_IAM
