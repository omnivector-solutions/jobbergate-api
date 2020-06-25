#!/bin/bash

set -e

export IS_OFFLINE="rats"
export DATABASE_NAME=`npx serverless dbName | awk '{print $3}'`
export DATABASE_USER=`npx serverless dbUser | awk '{print $3}'`
export DATABASE_PORT=`npx serverless dbPort | awk '{print $3}'`
export DATABASE_PASS=`npx serverless dbPass | awk '{print $3}'`
export DATABASE_HOST=`npx serverless dbHost | awk '{print $3}'`
export CLOUDFRONT_DOMAIN=`npx serverless domainInfo | awk '{print $3}'`
