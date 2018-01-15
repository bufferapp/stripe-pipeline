#!/usr/bin/env python

import os
import logging
import stripe
from datetime import datetime, timedelta
import transform
import write_data

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Crawler constants
DEFAULT_EVENT_START_DATE = datetime.today() - timedelta(days=1)
DEFAULT_EVENT_END_DATE = datetime.now().replace(second=0, microsecond=0)
DEFAULT_EVENT_TYPE_FILTER = 'customer.subscription.*'

stripe.api_key = os.environ.get('STRIPE_API_KEY')


def dict_filter_for_range(start, end):
    start = int(start.timestamp())
    end = int(end.timestamp())
    return {"gte": start, "lt": end}


def stripe_events_for_range(start_date=DEFAULT_EVENT_START_DATE,
                            end_date=DEFAULT_EVENT_END_DATE,
                            filter=DEFAULT_EVENT_TYPE_FILTER):
    created_range = dict_filter_for_range(start_date, end_date)

    raw_events = stripe.Event.list(
        type=filter,
        created=created_range,
        limit=100
    )

    return (e for e in raw_events.auto_paging_iter())


def main():
    start_date = datetime.today() - timedelta(days=180)
    end_date = datetime.now()
    events = stripe_events_for_range(start_date, end_date)

    with write_data.ChunkWriter() as writer:
        for i, event in enumerate(events):
            writer.write(transform.transform_subscription_event(event))


if __name__ == '__main__':
    main()
