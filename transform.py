from field_mapper import FieldMapper


def map_subscription(input, output, prefix):
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
            .map('plan_amount')
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
    sub_plan = sub.get('plan')
    previous_sub = event.data.get('previous_attributes')
    output = {}

    (FieldMapper(event, output)
        .map('id')
        .map('api_version')
        .map_ts('created')
        .map('type')
        .map('livemode')
        .map('pending_webhooks'))

    if event_request:
        FieldMapper(event_request, output).map('id', 'request')

    map_subscription(sub, output, 'subscription')

    if sub_plan:
        map_plan(sub_plan, output, 'subscription_plan')

    if previous_sub:
        map_subscription(previous_sub, output, 'previous_subscription')

    return output
