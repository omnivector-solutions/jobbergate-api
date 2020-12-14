#!/usr/bin/env python

# export a shell environment suitable for running the django app

import json
from shlex import quote
from subprocess import PIPE, STDOUT, run

import boto3
import click


STACK_NAME = "jobbbergate-api-{stage}"

# map the output name to a shell variable name that django wants
INTERESTING_OUTPUTS = {
    # these are AWS CF outputs
    "dbName": "DATABASE_NAME",
    "dbHost": "DATABASE_HOST",
    "dbPort": "DATABASE_PORT",
    "dbUri": "DATABASE_URI",
    "dbUser": "DATABASE_USER",
    "dbPass": "DATABASE_PASS",
    "assetsDistribution": "CLOUDFRONT_DOMAIN",
    # these are from serverless print
    "STAGE": "STAGE",
    "REGISTER_VERIFICATION_URL": "REGISTER_VERIFICATION_URL",
    "SENDGRID_API_KEY": "SENDGRID_API_KEY",
}


def print_export(key, val):
    """
    Print a properly-quoted shell variable
    """
    print(f"export {key}={quote(val)}")


def get_cloudformation_environmentals(stage):
    """
    key:value of each interesting variable from the cloudformation stack outputs
    """
    client = boto3.client("cloudformation")
    outputs = client.describe_stacks(StackName=STACK_NAME.format(**locals()))["Stacks"][
        0
    ]["Outputs"]
    outputs_dict = {}
    for o in outputs:
        k = o["OutputKey"]
        if k not in INTERESTING_OUTPUTS:
            continue

        v = o["OutputValue"]

        outputs_dict[INTERESTING_OUTPUTS[k]] = v

    return outputs_dict


def get_serverless_environmentals(stage):
    """
    key_value of each interesting variable from the serverless print info
    """
    ret = run(
        f"npx serverless print --format json --stage {quote(stage)}",
        shell=True,
        stderr=STDOUT,
        stdout=PIPE,
    )
    data = json.loads(ret.stdout)["provider"]["environment"]
    ret = {}
    for k, v in data.items():
        if k in INTERESTING_OUTPUTS:
            ret[k] = v

    return ret


@click.argument("stage")
@click.command("serverlessenv")
def main(stage):
    print_export("LAMBDA_TASK_ROOT", f"placeholder-xxx-{stage}")

    cf_env = get_cloudformation_environmentals(stage)
    for k, v in cf_env.items():
        print_export(k, v)

    sls_env = get_serverless_environmentals(stage)
    for k, v in sls_env.items():
        print_export(k, v)


main()
