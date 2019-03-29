import logging
import time
from datetime import datetime, timedelta
from dateutil import parser
import click
from stripe_pipeline import stripe_events
from stripe_pipeline import redshift
from stripe_pipeline.write_data import MB
from stripe_pipeline.process import SubscriptionEventsProcessor
from stripe_pipeline.process import ChargeEventsProcessor


logger = logging.getLogger()
logger.setLevel(logging.INFO)

MIDNIGHT_TODAY = datetime.now().replace(minute=0, second=0, microsecond=0)

def run_events_backfill(config, start=MIDNIGHT_TODAY, end=datetime.now(), chunk_size=10):
    events = stripe_events.stripe_events_for_range(start, end, config['filter'])
    chunk_size = chunk_size * MB

    processor = config['processor'](events, chunk_size)
    processor.process_events()


def run_subscription_events_backfill(start=MIDNIGHT_TODAY, end=datetime.now(), chunk_size=10):
    events = stripe_events.stripe_events_for_range(start, end)
    chunk_size = chunk_size * MB

    processor = SubscriptionEventsProcessor(events, chunk_size)
    processor.process_events()


def run_charge_events_backfill(start=MIDNIGHT_TODAY, end=datetime.now(), chunk_size=10):
    events = stripe_events.stripe_events_for_range(start, end, 'charge.*')
    chunk_size = chunk_size * MB

    processor = ChargeEventsProcessor(events, chunk_size)
    processor.process_events()

event_type_config = {
    'subscriptions': {
        'table_name': 'subscription_events',
        'filter': 'customer.subscription.*',
        'processor': SubscriptionEventsProcessor
    },
    'charges': {
        'table_name': 'charge_events',
        'filter': 'charge.*',
        'processor': ChargeEventsProcessor
    },
}

@click.command('backfill')
@click.option('--event-type', type=click.Choice(['subscriptions', 'charges']),
    default='subscription')
@click.option('--start', default=MIDNIGHT_TODAY,
              help='Filter events created after this timestamp')
@click.option('--end', default=datetime.now(),
              help='Filter events created before this timestamp')
@click.option('--chunk-size', default=10,
              help='The size (mb) of chunks to write data to Redshift')
def backfill(event_type, start, end, chunk_size):
    if isinstance(start, str):
        start = parser.parse(start)
    if isinstance(end, str):
        end = parser.parse(end)

    config = event_type_config.get(event_type)
    if not config:
        click.echo(f'Can''t backfill events of type {event_type}')
    else:
        run_events_backfill(config)

@click.command('run')
@click.option('--event-type', type=click.Choice(['subscriptions', 'charges']),
    default='subscription')
@click.option('--chunk-size', default=10,
              help='The size (mb) of chunks to write data to Redshift')
def run(event_type, chunk_size):
    config = event_type_config.get(event_type)
    if not config:
        click.echo(f'Can''t backfill events of type {event_type}')
    else:
        while(True):
            logger.info("Fetching the last seen event timestamp")
            start = redshift.get_latest_timestamp(config['table_name'])

            start = start - timedelta(seconds=1)  # 1s offset to avoid missing data
            end = datetime.now()
            run_events_backfill(config, start, end, chunk_size)

            logger.info("Loaded events starting from {}.".format(start))

            if (datetime.now() - end).total_seconds() < 60:
                logger.info("Last backfill within 1 minute. Sleeping for 1 minute")
                time.sleep(60)  # Sleep for a minute before checking for new data


@click.group('crawler')
def crawler():
    pass


crawler.add_command(run)
crawler.add_command(backfill)
