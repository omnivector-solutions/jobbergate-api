#!/usr/bin/env python3
"""
Edit AWS SSM parameters in a text editor and save them
"""
import inspect
import secrets
import string
import sys

import boto3
from botocore.exceptions import ClientError
import click
from codado import hotedit
import toml


PASSWORD_CHARS = string.ascii_letters + string.digits

PARAM_KEYS = (
    "DATABASE_NAME",
    "DATABASE_USER",
    "DATABASE_PASS",
    "REGISTER_VERIFICATION_URL",
    "SENTRY_DSN",
)

PARAM_TEMPLATE = inspect.cleandoc(
    """
    # {region} / {stage}

    [ssm]
    DATABASE_NAME = {DATABASE_NAME!a}
    DATABASE_PASS = {DATABASE_PASS!a}
    DATABASE_USER = {DATABASE_USER!a}
    REGISTER_VERIFICATION_URL = {REGISTER_VERIFICATION_URL!a}
    SENTRY_DSN = {SENTRY_DSN!a}
    """
)

REGION_CHOICES = (
    "us-west-2",
    "eu-north-1",
)


def make_password(charset=PASSWORD_CHARS):
    """
    Generate a secure password
    """
    return "".join(secrets.choice(charset) for i in range(20))


def read_upstream(client, stage):
    """
    Get a bunch of SSM Parameters from AWS
    """
    defaults = dict(
        DATABASE_NAME="jobbergate",
        DATABASE_USER="omnivector",
        DATABASE_PASS=make_password(),
    )

    prefix = f"/jobbergate-api/{stage}"
    for k in PARAM_KEYS:
        try:
            val = client.get_parameter(Name=f"{prefix}/{k}")["Parameter"]["Value"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "ParameterNotFound":
                val = defaults.get(k, "")
            else:
                raise

        yield (k, val)


def save_upstream(client, stage, data):
    """
    Put a bunch of param values into AWS
    """
    prefix = f"/jobbergate-api/{stage}"
    for k, v in data.items():
        client.put_parameter(
            Name=f"{prefix}/{k}",
            Value=v,
            Type="String",
            Overwrite=True,
        )
        yield (k, v)


@click.command()
@click.pass_context
@click.option("--region", "-r", default="us-west-2", type=click.Choice(REGION_CHOICES))
@click.argument("stage", type=str)
def ssmparameters(ctx: click.Context, region, stage):
    """
    Edit AWS SSM parameters in a text editor and save them
    """
    client = boto3.client("ssm", region_name=region)

    orig = {}
    for (k, v) in read_upstream(client, stage):
        orig.update({k: v})
        click.echo(".", nl=False)

    click.echo("")

    orig_file = PARAM_TEMPLATE.format(**orig, stage=stage, region=region)

    while True:
        try:
            new_file = hotedit.hotedit(initial=orig_file, validate_unchanged=True)
        except hotedit.Unchanged:
            click.echo("** Parameters were unchanged", file=sys.stderr)
            if click.confirm("Try again?"):
                continue
            else:
                ctx.exit(1)

        new_data = toml.loads(new_file)
        # sanity check that we've only seen the keys we want to see
        check_keys = sorted(new_data.get("ssm", {}).keys())
        if not check_keys == sorted(PARAM_KEYS):
            click.echo(f"** Error: some unexpected parameters (saw: {check_keys})")
            if click.confirm("Try again?"):
                orig_file = new_file
                continue
            else:
                ctx.exit(1)

        break

    for _ in save_upstream(client, stage, new_data["ssm"]):
        click.echo(".", nl=False)
    click.echo("Saved.")


ssmparameters()
