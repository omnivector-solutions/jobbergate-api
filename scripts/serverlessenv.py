#!/usr/bin/env python

# export a shell environment suitable for running the django app

import os
from shlex import quote

import boto3
import click


REGION_CHOICES = (
    "us-west-2",
    "eu-north-1",
)

STACK_NAME = "jobbergate-api-{stage}"

# map the output name to a shell variable name that django wants
AWS_CF_OUTPUTS = {
    "dbName": "DATABASE_NAME",
    "dbHost": "DATABASE_HOST",
    "dbPort": "DATABASE_PORT",
    "dbUri": "DATABASE_URI",
    "dbUser": "DATABASE_USER",
    "dbPass": "DATABASE_PASS",
    "assetsDistribution": "CLOUDFRONT_DOMAIN",
}

AWS_SSM_PARAMETERS = {
    "REGISTER_VERIFICATION_URL": "REGISTER_VERIFICATION_URL",
    "JOBBERGATE_SECRET_KEY": "JOBBERGATE_SECRET_KEY",
}


def print_export(key, val):
    """
    Print a properly-quoted shell variable
    """
    print(f"export {key}={quote(val)}")


def get_cloudformation_environmentals(stage):
    """
    key:value of each variable from the cloudformation stack outputs that we need
    """
    client = boto3.client("cloudformation")
    outputs = client.describe_stacks(StackName=STACK_NAME.format(**locals()))["Stacks"][
        0
    ]["Outputs"]
    environmentals = {}
    for o in outputs:
        k = o["OutputKey"]
        if k not in AWS_CF_OUTPUTS:
            continue

        v = o["OutputValue"]

        environmentals[AWS_CF_OUTPUTS[k]] = v

    return environmentals


def get_parameterstore_environmentals(stage):
    """
    key:value of each variable from ssm parameter store that we need
    """
    client = boto3.client("ssm")
    prefix = f"/jobbergate-api/{stage}"
    environmentals = {}
    for ssmname, envname in AWS_SSM_PARAMETERS.items():
        val = client.get_parameter(Name=f"{prefix}/{ssmname}")
        environmentals[envname] = val["Parameter"]["Value"]

    return environmentals


@click.option("--region", "-r", default="us-west-2", type=click.Choice(REGION_CHOICES))
@click.argument("stage", type=str)
@click.command("serverlessenv")
def main(region, stage):
    print_export("AWS_DEFAULT_REGION", region)
    print_export("LAMBDA_TASK_ROOT", f"placeholder-xxx-{stage}")
    print_export("SERVERLESS_STAGE", stage)
    print_export("SERVERLESS_REGION", region)

    # boto calls after this point will use the correct region
    os.environ["AWS_DEFAULT_REGION"] = region

    cf_env = get_cloudformation_environmentals(stage)
    ssm_env = get_parameterstore_environmentals(stage)
    for k, v in {**cf_env, **ssm_env}.items():
        print_export(k, v)


main()
