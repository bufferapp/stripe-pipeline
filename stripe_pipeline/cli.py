#!/usr/bin/env python

import click
from stripe_pipeline.crawler import crawler


@click.group()
def cli():
    pass


cli.add_command(crawler)

if __name__ == '__main__':
    cli()
