#!/bin/bash

set -e

stage=$1

export LAMBDA_TASK_ROOT="rats"
export DATABASE_NAME=`npx serverless dbName --stage $stage | awk '{print $3}'`
export DATABASE_USER=`npx serverless dbUser --stage $stage | awk '{print $3}'`
export DATABASE_PORT=`npx serverless dbPort --stage $stage | awk '{print $3}'`
export DATABASE_PASS=`npx serverless dbPass --stage $stage | awk '{print $3}'`
export DATABASE_HOST=`npx serverless dbHost --stage $stage | awk '{print $3}'`
export CLOUDFRONT_DOMAIN=`npx serverless domainInfo --stage $stage | awk '{print $3}'`
