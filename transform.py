import hashlib
from field_mapper import FieldMapper


def hash(*fields):
    fields_str = ''.join(fields).encode('utf-8')
    return hashlib.md5(fields_str).hexdigest()


def map_subscription(input, output, prefix):
    sub_plan = input.get('plan')

    if sub_plan:
        map_plan(sub_plan, output, '{}_plan'.format(prefix))

    return (FieldMapper(input, output, prefix)
            .map('id')
            .map_ts('created')
            .map_ts('current_period_end')
            .map_ts('current_period_start')
            .map_id('customer')
            .map('livemode')
            .map('quantity')
            .map_ts('start')
            .map('status')
            .map('billing')
            .map_ts('trial_end')
            .map_ts('trial_start')
            .map('cancel_at_period_end')
            .map_ts('canceled_at'))


def map_plan(input, output, prefix):
    return (FieldMapper(input, output, prefix)
            .map('id')
            .map('amount')
            .map_ts('created')
            .map('currency')
            .map('interval')
            .map('interval_count')
            .map('livemode')
            .map('name')
            .map('statement_descriptor'))


def transform_subscription_event(event):
    event_request = event.get('request')

    sub = event.data.object
    previous_sub = event.data.get('previous_attributes')
    event_output = {}

    (FieldMapper(event, event_output)
        .map('id')
        .map('api_version')
        .map_ts('created')
        .map('type')
        .map('livemode')
        .map('pending_webhooks'))

    if event_request:
        FieldMapper(event_request, event_output).map('id', 'request')

    map_subscription(sub, event_output, 'subscription')

    if previous_sub:
        map_subscription(previous_sub, event_output, 'previous_subscription')

    return event_output


def transform_subscription_event_items(event):
    sub = event.data.object
    previous_sub = event.data.get('previous_attributes', {})

    sub_items = sub.get('items', {}).get('data', [])
    sub_previous_items = previous_sub.get('items', {}).get('data', [])

    all_items = sub_items + sub_previous_items
    item_ids = set([i.id for i in all_items])

    def match_item(items, item_id):
        return next((i for i in items if i.id == item_id), None)

    output_records = []

    for item_id in item_ids:
        record_output = {}
        (FieldMapper(event, record_output)
            .map('id', output_transform=lambda i: hash(i, item_id))
            .map('id', 'event_id')
            .map_ts('created'))

        sub_item = match_item(sub_items, item_id)
        if sub_item:
            map_subscription(sub_item, record_output, 'item')

        previous_item = match_item(sub_previous_items, item_id)
        if previous_item:
            map_subscription(previous_item, record_output, 'previous_item')

        output_records.append(record_output)

    return output_records
