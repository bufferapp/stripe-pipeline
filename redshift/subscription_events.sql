drop table if exists "buda_stripe"."subscription_events";
create table "buda_stripe"."subscription_events"
(
	"id" varchar(18)   encode lzo
	,"api_version" varchar(12)   encode lzo
	,"created_at" timestamp without time zone   encode lzo
	,"type" varchar(50)   encode lzo
	,"subscription_id" varchar(18)   encode lzo
	,"subscription_created_at" timestamp without time zone   encode lzo
	,"subscription_current_period_end_at" timestamp without time zone   encode lzo
	,"subscription_current_period_start_at" timestamp without time zone   encode lzo
	,"subscription_customer_id" varchar(18)   encode lzo
	,"subscription_livemode" boolean
	,"subscription_plan_id" varchar(100)   encode lzo
	,"subscription_plan_amount" integer   encode lzo
	,"subscription_plan_created_at" timestamp without time zone   encode lzo
	,"subscription_plan_currency" varchar(3)   encode lzo
	,"subscription_plan_interval" varchar(5)   encode lzo
	,"subscription_plan_interval_count" integer   encode lzo
	,"subscription_plan_livemode" boolean
	,"subscription_plan_name" varchar(400)   encode lzo
	,"subscription_plan_statement_descriptor" varchar(400)   encode lzo
	,"subscription_plan_statement_description" varchar(400)   encode lzo
	,"subscription_quantity" integer   encode lzo
	,"subscription_start_at" timestamp without time zone   encode lzo
	,"subscription_status" varchar(8)   encode lzo
	,"subscription_billing" varchar(20)   encode lzo
	,"livemode" boolean
	,"previous_subscription_current_period_end_at" timestamp without time zone   encode lzo
	,"previous_subscription_current_period_start_at" timestamp without time zone   encode lzo
	,"request" varchar(18)   encode lzo
	,"subscription_trial_end_at" timestamp without time zone   encode lzo
	,"subscription_trial_start_at" timestamp without time zone   encode lzo
	,"previous_subscription_plan_id" varchar(100)   encode lzo
	,"previous_subscription_plan_amount" integer   encode lzo
	,"previous_subscription_plan_created_at" timestamp without time zone   encode lzo
	,"previous_subscription_plan_currency" varchar(3)   encode lzo
	,"previous_subscription_plan_interval" varchar(5)   encode lzo
	,"previous_subscription_plan_interval_count" integer   encode lzo
	,"previous_subscription_plan_livemode" boolean
	,"previous_subscription_plan_name" varchar(400)   encode lzo
	,"previous_subscription_plan_statement_descriptor" varchar(400)   encode lzo
	,"previous_subscription_plan_statement_description" varchar(400)   encode lzo
	,"previous_subscription_start_at" timestamp without time zone   encode lzo
	,"previous_subscription_trial_end_at" timestamp without time zone   encode lzo
	,"previous_subscription_status" varchar(8)   encode lzo
	,"subscription_cancel_at_period_end" boolean
	,"subscription_canceled_at" timestamp without time zone   encode lzo
	,"previous_subscription_trial_start_at" timestamp without time zone   encode lzo
	,"previous_subscription_cancel_at_period_end" boolean
	,"previous_subscription_canceled_at" timestamp without time zone   encode lzo
	,"previous_subscription_quantity" integer   encode lzo
	,"pending_webhooks" integer encode lzo
)
diststyle even
;
