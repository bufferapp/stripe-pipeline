# Stripe Event Pipeline

This is the first working version of a simple pipeline to extract Stripe
Events using the API and store them in Redshift.

This initial version only works with Stripe Subscription Events and
ignores Subscription Items and Metadata.

It was successfully used to backfill a period of data needed for ad-hoc
analysis.

We plan on adding further functionality to this pipeline:

- Support pulling in all the subscription event data
- More events like invoices, charges, etc. Ideally we can pull in all
event types at some point
- Smarter loading logic, support for resuming from last data in Redshift
- Compressing data before loading to Redshift to decreasing bandwith
used
- More robust error handling

