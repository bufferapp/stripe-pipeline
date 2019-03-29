drop table if exists "buda_stripe"."charge_events";
create table "buda_stripe"."charge_events"
(
	"id" varchar(18)   encode lzo
	,"api_version" varchar(12)   encode lzo
	,"created_at" timestamp without time zone   encode lzo
	,"type" varchar(50)   encode lzo
	,"livemode" boolean
	,"charge_id" varchar(18)   encode lzo
	,"charge_created_at" timestamp without time zone   encode lzo
	,"charge_amount" integer
	,"amount_refunded" integer
	,"charge_balance_transaction" varchar(20)
	,"charge_captured" boolean
	,"charge_currency" varchar(3)
	,"charge_customer" varchar (20)
	,"charge_description" varchar(100)
	,"charge_destination" varchar(100)
	,"charge_dispute" varchar(100)
	,"charge_failure_code" integer
	,"charge_failure_message" varchar(200)
	,"charge_invoice" varchar(20)
	,"charge_paid" boolean
	,"charge_receipt_number" varchar(100)
	,"charge_refunded" boolean
	,"charge_statement_descriptor" varchar(100)
	,"charge_status" varchar(8)
	, "pending_webhooks" integer encode lz
)