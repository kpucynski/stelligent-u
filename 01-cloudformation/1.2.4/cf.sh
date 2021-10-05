#!/usr/bin/env bash

REGION="${2:-us-east-2}"


aws cloudformation $1-stack --stack-name kpu-lab-02  --region ${REGION}

# Export PolicyArn cannot be deleted as it is in use by kpu-lab-02-1

aws cloudformation $1-stack --stack-name kpu-lab-02-1  --region ${REGION}
aws cloudformation $1-stack --stack-name kpu-lab-02  --region ${REGION}

