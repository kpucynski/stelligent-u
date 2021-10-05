#!/usr/bin/env python3

import boto3
import botocore
import json
import yaml
import sys

def create_clients(regions):
  clients = []
  for region in regions:
    client = boto3.client('cloudformation', region_name=region)
    clients.append(client)
  return clients

def create_stack(client, stack_name, template, parameters):
  print("Creating stack "+stack_name+" in "+client.meta.region_name+"...")
  response = client.create_stack(
    StackName = stack_name,
    TemplateBody = template,
    Parameters = parameters
  )
  return response

def update_stack(client, stack_name, template, parameters):
  print("Updating stack "+stack_name+" in "+client.meta.region_name+"...")
  response = client.update_stack(
    StackName = stack_name,
    TemplateBody = template,
    Parameters = parameters
  )
  return response

def delete_stack(client, stack_name, template, parameters):
  print("Deleting stack "+stack_name+" in "+client.meta.region_name+"...")
  response = client.delete_stack(
    StackName = stack_name,
  )
  return response 

def check_stack_exist(client, stack_name):
  print("Checking stack "+stack_name+"...")
  stacks = client.list_stacks()['StackSummaries']
  for stack in stacks:
    if stack['StackStatus'] == 'DELETE_COMPLETE':
      # Stack name exists but it is deleted, skip
      continue
    if stack_name == stack['StackName']:
      return True
  return False

def main():
  action=""
  if len(sys.argv) > 1:
    action = sys.argv[1]
  
  stack_name = 'kpu-lab-03'

  config = json.load(open('./regions.json'))

  regions = []
  for r in config['Regions']:
    regions.append(r['RegionName'])
  
  clients = create_clients(regions)

  with open("./s3.yaml",'r') as fileobj:
    template = fileobj.read()
 
  parameters = json.load(open('./s3.json'))

  if action == "create":
    for client in clients:
      if check_stack_exist(client, stack_name):
        print("Stack exist, updating...")
        try:
          update_stack(client, stack_name, template, parameters)
        except Exception as e:
          print(e)
      else:
        print("Stack does not exist, creating...")
        try:
          create_stack(client, stack_name, template, parameters)
        except Exception as e:
          print(e)
  elif action == "delete" :
    for client in clients:
      try:
        delete_stack(client, stack_name, template, parameters)
      except Exception as e:
        print(e)
  else:
    print("Usage: "+__file__+" [create|delete]")

if __name__ == "__main__":
	main()
