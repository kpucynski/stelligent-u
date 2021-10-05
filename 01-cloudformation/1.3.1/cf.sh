#!/usr/bin/env bash

set -eou pipefail

ACTION=${1:-create}
CONFIG='regions.json'
STACK='kpu-lab-03'

REGIONS="$(cat $CONFIG | jq -r '.Regions[].RegionName')"

create(){
    for REGION in ${REGIONS}; do
      echo "Creating ${STACK} in ${REGION}..."
      aws cloudformation ${ACTION}-stack --stack-name ${STACK} \
          --template-body file://s3.yaml --parameters file://s3.json --region ${REGION} | jq .
    done;
}

delete(){
  for REGION in ${REGIONS}; do
    echo "Deleting ${STACK} in ${REGION}"
    aws cloudformation delete-stack --stack-name ${STACK}  --region ${REGION} | jq .
  done;
}

case ${ACTION} in
  create)
    create
    ;;
  update)
    update
    ;;
  delete)
    delete
    ;;
  *)
    echo "Usage $0 [create|update|delete]"
    ;;
esac
