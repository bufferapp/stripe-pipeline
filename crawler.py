#!/usr/bin/env python

import logging
import stripe_events
from datetime import datetime
from dateutil import parser
import click
from write_data import MB
from process import SubscriptionEventsProcessor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

MIDNIGHT_TODAY = datetime.now().replace(minute=0, second=0, microsecond=0)


@click.group()
def cli():
    pass


def run_backfill(start=MIDNIGHT_TODAY, end=datetime.now(), chunk_size=10):
    events = stripe_events.stripe_events_for_range(start, end)
    chunk_size = chunk_size * MB

    processor = SubscriptionEventsProcessor(events, chunk_size)
    processor.process_events()


@click.command('backfill')
@click.option('--start', default=MIDNIGHT_TODAY,
              help='Filter events created after this timestamp')
@click.option('--end', default=datetime.now(),
              help='Filter events created before this timestamp')
@click.option('--chunk-size', default=10,
              help='The size (mb) of chunks to write data to Redshift')
def backfill(start, end, chunk_size):
    if isinstance(start, str):
        start = parser.parse(start)
    if isinstance(end, str):
        end = parser.parse(end)

    run_backfill(start, end, chunk_size)


cli.add_command(backfill)

if __name__ == '__main__':
    cli()
