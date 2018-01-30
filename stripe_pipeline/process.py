from stripe_pipeline.transform import transform_subscription_event, \
     transform_subscription_event_items

from stripe_pipeline.write_data import ChunkWriter


class SubscriptionEventsProcessor():
    def __init__(self, events, chunk_size):
        self.events = events
        self.chunk_size = chunk_size

    def writer(self, name):
        return ChunkWriter(name, chunk_size=self.chunk_size)

    def process_events(self):
        with self.writer('subscription_events') as subscription_events, \
                self.writer('subscription_event_items') as event_items:
            for event in self.events:
                subscription_events.write_record(
                    transform_subscription_event(event)
                )

                event_items.write_records(
                    transform_subscription_event_items(event)
                )
