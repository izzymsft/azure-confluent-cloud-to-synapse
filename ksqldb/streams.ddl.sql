
CREATE STREAM IF NOT EXISTS product_changes (
    product_id INT KEY,
    product_name STRING,
    product_price DOUBLE,
    coupon_code STRING,
    product_description STRING,
    active_product INT
) WITH (
    KAFKA_TOPIC = 'productchanges',
    KEY_FORMAT = 'JSON',
    VALUE_FORMAT='JSON'
);

PRINT productchanges FROM BEGINNING;

DROP STREAM IF EXISTS contoso_products;

CREATE OR REPLACE STREAM contoso_products
WITH (
    KEY_FORMAT = 'AVRO',
    VALUE_FORMAT='AVRO',
    KAFKA_TOPIC='jordan'
) AS SELECT product_id, product_name, product_price, coupon_code, product_description, active_product
FROM product_changes;

PRINT contoso_products FROM BEGINNING;

DROP STREAM IF EXISTS contoso_products;

CREATE STREAM IF NOT EXISTS contoso_products (
    product_id INT KEY,
    product_name STRING,
    product_price DOUBLE,
    coupon_code STRING,
    product_description STRING,
    active_product INT
) WITH (
    KAFKA_TOPIC = 'contosoproducts',
    KEY_FORMAT = 'AVRO',
    VALUE_FORMAT='AVRO',
    VALUE_SCHEMA_ID=100001
);