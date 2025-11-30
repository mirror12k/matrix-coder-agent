#!/bin/bash
set -e
echo '' > .env.temp

if [[ -z $(aws configure get aws_access_key_id) ]]; then
    echo "no aws credentials found. skipping configuration..."
    exit
fi

AWS_USERNAME=$(aws sts get-caller-identity | jq -r '.Arn | split("/")[1]')
AWS_MFA_DEVICE_ARN=$(aws iam list-mfa-devices --user-name "$AWS_USERNAME" | jq -r '.MFADevices[0].SerialNumber')

if [[ "$AWS_MFA_DEVICE_ARN" != "null" ]]; then
    echo -n "please enter your mfa token for device $AWS_MFA_DEVICE_ARN: "

    MFA_TOKEN=""
    while IFS= read -r -s -n 1 c; do
        if [[ $c == $'\0' ]]; then
            break
        fi
        MFA_TOKEN="${MFA_TOKEN}$c"
        echo -n "*"
    done
    echo

    AWS_CREDS=$(aws sts get-session-token --serial-number "$AWS_MFA_DEVICE_ARN" --token-code "$MFA_TOKEN" --duration-seconds 7200)
    AWS_ACCESS_KEY_ID=$(echo "$AWS_CREDS" | jq -r ".Credentials.AccessKeyId")
    AWS_SECRET_ACCESS_KEY=$(echo "$AWS_CREDS" | jq -r ".Credentials.SecretAccessKey")
    AWS_SESSION_TOKEN=$(echo "$AWS_CREDS" | jq -r ".Credentials.SessionToken")
    echo "aws configured with 2-hour temporary credentials: $AWS_ACCESS_KEY_ID"
    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> .env.temp
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env.temp
    echo "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN" >> .env.temp

    exit
else
    echo "no mfa device found, configuring with fixed credentials"
    echo "  warning: you will not be able to call any IAM apis with these credentials!"

    AWS_CREDS=$(aws sts get-session-token --duration-seconds 7200)
    AWS_ACCESS_KEY_ID=$(echo "$AWS_CREDS" | jq -r ".Credentials.AccessKeyId")
    AWS_SECRET_ACCESS_KEY=$(echo "$AWS_CREDS" | jq -r ".Credentials.SecretAccessKey")
    AWS_SESSION_TOKEN=$(echo "$AWS_CREDS" | jq -r ".Credentials.SessionToken")
    echo "aws configured with 2-hour temporary credentials: $AWS_ACCESS_KEY_ID"
    echo "AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID" >> .env.temp
    echo "AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY" >> .env.temp
    echo "AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN" >> .env.temp
    exit
fi
