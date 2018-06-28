#!/usr/bin/env python

import click
from stripe_pipeline.crawler import crawler


@click.group()
def main():
    pass


main.add_command(crawler)

if __name__ == '__main__':
    main()
