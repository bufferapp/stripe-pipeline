import os
import logging
import stripe
from datetime import datetime, timedelta
stripe.api_key = os.environ.get('STRIPE_API_KEY')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DEFAULT_EVENT_START_DATE = datetime.today() - timedelta(days=1)
DEFAULT_EVENT_END_DATE = datetime.now().replace(second=0, microsecond=0)
DEFAULT_EVENT_TYPE_FILTER = 'customer.subscription.*'


def dict_filter_for_range(start, end):
    start = int(start.timestamp())
    end = int(end.timestamp())
    return {"gte": start, "lt": end}


def stripe_events_for_range(start_date=DEFAULT_EVENT_START_DATE,
                            end_date=DEFAULT_EVENT_END_DATE,
                            filter=DEFAULT_EVENT_TYPE_FILTER,
                            ending_before_id=None):

    logger.info("Fetching stripe events between {} and {}"
                .format(start_date, end_date))
    created_range = dict_filter_for_range(start_date, end_date)
    args = {
        'type': filter,
        'created': created_range,
        'limit': 100
    }

    if ending_before_id:
        del(args['created'])
        args['ending_before'] = ending_before_id

    raw_events = stripe.Event.list(**args)

    return (e for e in raw_events.auto_paging_iter())
