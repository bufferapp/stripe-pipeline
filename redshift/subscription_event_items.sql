drop table if exists "buda_stripe"."subscription_event_items";
create table "buda_stripe"."subscription_event_items"
(
	"id" varchar(18)   encode lzo
	, "event_id" varchar(12)   encode lzo
	, "created_at" timestamp without time zone   encode lzo
	, "item_id" varchar(18)   encode lzo
	, "item_created_at" timestamp without time zone   encode lzo
	, "item_current_period_end_at" timestamp without time zone   encode lzo
	, "item_current_period_start_at" timestamp without time zone   encode lzo
	, "item_customer_id" varchar(18)   encode lzo
	, "item_livemode" boolean
	, "item_plan_id" varchar(100)   encode lzo
	, "item_plan_amount" integer   encode lzo
	, "item_plan_created_at" timestamp without time zone   encode lzo
	, "item_plan_currency" varchar(3)   encode lzo
	, "item_plan_interval" varchar(5)   encode lzo
	, "item_plan_interval_count" integer   encode lzo
	, "item_plan_livemode" boolean
	, "item_plan_name" varchar(400)   encode lzo
	, "item_plan_statement_descriptor" varchar(400)   encode lzo
	, "item_plan_statement_description" varchar(400)   encode lzo
	, "item_quantity" integer   encode lzo
	, "item_start_at" timestamp without time zone   encode lzo
	, "item_status" varchar(8)   encode lzo
	, "item_billing" varchar(20)   encode lzo
	, "item_trial_end_at" timestamp without time zone   encode lzo
	, "item_trial_start_at" timestamp without time zone   encode lzo
	, "previous_item_plan_id" varchar(100)   encode lzo
	, "previous_item_current_period_end_at" timestamp without time zone   encode lzo
	, "previous_item_current_period_start_at" timestamp without time zone   encode lzo
	, "previous_item_plan_amount" integer   encode lzo
	, "previous_item_plan_created_at" timestamp without time zone   encode lzo
	, "previous_item_plan_currency" varchar(3)   encode lzo
	, "previous_item_plan_interval" varchar(5)   encode lzo
	, "previous_item_plan_interval_count" integer   encode lzo
	, "previous_item_plan_livemode" boolean
	, "previous_item_plan_name" varchar(400)   encode lzo
	, "previous_item_plan_statement_descriptor" varchar(400)   encode lzo
	, "previous_item_plan_statement_description" varchar(400)   encode lzo
	, "previous_item_start_at" timestamp without time zone   encode lzo
	, "previous_item_trial_end_at" timestamp without time zone   encode lzo
	, "previous_item_status" varchar(8)   encode lzo
	, "previous_item_cancel_at_period_end" boolean
	, "previous_item_canceled_at" timestamp without time zone   encode lzo
	, "previous_item_trial_start_at" timestamp without time zone   encode lzo
	, "previous_item_cancel_at_period_end" boolean
	, "previous_item_canceled_at" timestamp without time zone   encode lzo
	, "previous_item_quantity" integer   encode lzo
)
diststyle even
;
