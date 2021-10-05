#!/usr/bin/env python3

profile = 'stelligent'
target_profile='stelligent-mfa'
arn = 'arn:aws:iam::324320755747:mfa/karol.pucynski.labs'

import os
import json
import argparse
import subprocess
import configparser

parser = argparse.ArgumentParser(description='AWS CLI temporary creds')
parser.add_argument('token', help='MFA token')
parser.add_argument('--profile', help='aws profile', default=profile)
parser.add_argument('--arn', help='AWS MFA ARN', default=arn)
parser.add_argument('--credential-path', help='AWS credentials file', default=os.path.expanduser('~/.aws/credentials'))

args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.credential_path)

if args.profile not in config.sections():
    parser.error('Invalid profile')

config[target_profile]['aws_arn_mfa'] = args.arn

result = subprocess.run(['aws', 'sts', 'get-session-token', '--profile', args.profile, '--serial-number', args.arn,
                         '--token-code', args.token], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if result.returncode != 0:
    parser.error(result.stderr.decode('utf-8').strip('\n'))

credentials = json.loads(result.stdout.decode('utf-8'))['Credentials']

config[target_profile]['aws_access_key_id'] = credentials['AccessKeyId']
config[target_profile]['aws_secret_access_key'] = credentials['SecretAccessKey']
config[target_profile]['aws_session_token'] = credentials['SessionToken']

with open(args.credential_path, 'w') as configFile:
    config.write(configFile)

print('Creds saved: ' + target_profile + ' to ' + args.credential_path)
print('Expiration: '+ credentials['Expiration'])
