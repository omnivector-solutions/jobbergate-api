#!/usr/bin/env python

# export a shell environment suitable for running the django app

from shlex import quote

import boto3
import click


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


@click.argument("stage")
@click.command("serverlessenv")
def main(stage):
    print_export("LAMBDA_TASK_ROOT", f"placeholder-xxx-{stage}")
    print_export("STAGE", stage)

    cf_env = get_cloudformation_environmentals(stage)
    ssm_env = get_parameterstore_environmentals(stage)
    for k, v in {**cf_env, **ssm_env}.items():
        print_export(k, v)


main()
