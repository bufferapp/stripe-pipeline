#!/usr/bin/env python

import os
import base64
import yaml
import click


def load_template():
    return yaml.load(open('kube/crawler.secrets.yaml.template', 'r'))


def assign(template, name, env_name):
    value = os.environ[env_name]
    encoded_value = base64.b64encode(value.encode()).decode()
    template['data'][name] = encoded_value
    return template


@click.command()
def make_secrets():
    """Convert the crawler.secrets.yaml.template file to a real secrets file"""
    template = load_template()

    assign(template, 'redshift-endpoint', 'REDSHIFT_ENDPOINT')
    assign(template, 'redshift-database', 'REDSHIFT_DB_NAME')
    assign(template, 'redshift-port', 'REDSHIFT_DB_PORT')
    assign(template, 'redshift-user', 'REDSHIFT_USER')
    assign(template, 'redshift-password', 'REDSHIFT_PASSWORD')
    assign(template, 'redshift-copy-s3-root', 'REDSHIFT_COPY_S3_ROOT')
    assign(template, 'aws-access-key-id', 'AWS_ACCESS_KEY_ID')
    assign(template, 'aws-secret-access-key', 'AWS_SECRET_ACCESS_KEY')
    assign(template, 'aws-default-region', 'AWS_DEFAULT_REGION')
    assign(template, 'stripe-api-key', 'STRIPE_API_KEY')

    click.echo(yaml.dump(template, default_flow_style=False))


if __name__ == '__main__':
    make_secrets()
