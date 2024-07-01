
DROP TABLE IF EXISTS product_data;
CREATE TABLE product_data
(
    product_id int NOT NULL PRIMARY KEY,
    product_name varchar(16),
    product_price float,
    coupon_code varchar(32),
    product_description varchar(max),
    active_product int NOT NULL
);

DROP TABLE IF EXISTS product_tracking;
CREATE TABLE product_tracking
(
    product_id int NOT NULL PRIMARY KEY,
    transaction_count int NOT NULL
);

SET IDENTITY_INSERT product_data ON;
SET IDENTITY_INSERT product_data OFF;


DROP TABLE IF EXISTS dbo.product_data_expanded;

CREATE TABLE dbo.product_data_expanded
(
    product_id int NOT NULL identity,
    product_name varchar(16),
    product_price float,
    coupon_code varchar(32),
    product_description varchar(max),
    active_product int NOT NULL,
    date_created datetime CONSTRAINT pde_date_created DEFAULT (GETUTCDATE()),
    date_modified datetime DEFAULT (GETUTCDATE())
);

DROP TRIGGER IF EXISTS product_data_expanded_modified_date;

CREATE TRIGGER product_data_expanded_modified_date
ON dbo.product_data_expanded
AFTER UPDATE 
AS
   UPDATE dbo.product_data_expanded
   SET date_modified = GETUTCDATE()
   FROM Inserted i
   WHERE dbo.product_data_expanded.product_id = i.product_id;