#!/usr/bin/env bash

REGION="${2:-us-east-2}"

#aws cloudformation update-termination-protection --stack-name kpu-lab-01 --region $REGION --enable-termination-protection
#aws cloudformation update-termination-protection --stack-name kpu-lab-01 --region $REGION --no-enable-termination-protection

aws cloudformation $1-stack --stack-name kpu-lab-01  --region ${REGION}
