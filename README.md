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


## Setup

1. Copy the `.env_template` file:
```
    cp .env_template .env
```

2. Fill out the `.env` file. You'll need Redshift connection details and credentials, AWS credentials and an S3 bucket location, as well as a Stripe API key

3. Set up a dev environment and install all the dependencies

```
make init
```

4. Create the table schema if it doesn't exist. Currently the only table to create is in `redshift/subscription_events.sql`

## Usage

After completing the setup, you should be able to run the crawler!

```
stripe-pipeline crawler run
```

Or:
```
make run
```


The `crawler run` command will query the database to find the last date an event was saved
in the subscription events table.

It will then backfill from that date up until now, after which it will keep polling stripe for new events
every minute and load them into the pipeline.

### Docker

The whole application can also be run within a Docker container.
To build a image and run the crawler in Docker:

```
make rund

```
