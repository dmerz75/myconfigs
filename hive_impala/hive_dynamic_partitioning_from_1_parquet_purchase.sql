-- hive_dynamic_partitioning_from_1_parquet.sql

--These are the steps to go from uploading 1 parquet file onto hdfs to
--registering a dynamically partitioned hive table.

-- 1. Create the unpartitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_purchasing_hist_r10
( `checkout_date` STRING, `merchant_id` BIGINT,`customer_id` BIGINT,`product_id` BIGINT,
  `product_name` STRING, `brand` STRING,`l_cat` STRING,`l1_cat` STRING,`l2_cat` STRING,
  `type_id` BIGINT, `type_name` STRING,`quantity` BIGINT,`price_mrp` DOUBLE,`order_id` BIGINT,
  checkout_date_part STRING )
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/purchase_hist_r14'

-- 2. Load data into the unpartitioned table.
load data inpath '/enterprise_data/dev/media_in/grofers/raw/purchase_hist_r14'
into table dd_media_in.grofers_purchasing_hist_r10

-- 3. Confirm the total count. (37095180)
select count(1) from dd_media_in.grofers_purchasing_hist_r10

-- 4. Set the dynamic partitioning configurations.
SET hive.exec.dynamic.partition = true
SET hive.exec.dynamic.partition.mode = nonstrict

-- 5. Create the partitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_purchasing_hist_p10 (
    `checkout_date` STRING, `merchant_id` BIGINT,`customer_id` BIGINT,`product_id` BIGINT,
    `product_name` STRING,`brand` STRING,`l_cat` STRING,`l1_cat` STRING,`l2_cat` STRING,
    `type_id` BIGINT,`type_name` STRING,`quantity` BIGINT,`price_mrp` DOUBLE,`order_id` BIGINT
    )
PARTITIONED BY (checkout_date_part STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/purchase_hist_p14'

-- 6. Insert the unpartitioned data into the partitioned table.
INSERT OVERWRITE TABLE dd_media_in.grofers_purchasing_hist_p10
PARTITION(checkout_date_part)
SELECT * FROM dd_media_in.grofers_purchasing_hist_r10

-- 7. Confirm the partitions in the partitioned table.
show partitions dd_media_in.grofers_purchasing_hist_p10

-- 8. Confirm the total count, unpartitioned vs partitioned table.
select count(1) from dd_media_in.grofers_purchasing_hist_p10

-- 9. Some final organization commands.
ALTER VIEW dd_media_in.grofers_purchasing_hist RENAME TO dd_media_in.grofers_purchasing_hist_v1

DROP VIEW dd_media_in.grofers_purchasing_hist

CREATE VIEW IF NOT EXISTS grofers_purchasing_hist AS SELECT * FROM grofers_purchasing_hist_p10

desc dd_media_in.grofers_purchasing_hist_p10

show partitions dd_media_in.grofers_purchasing_hist_p10
--1 checkout_date_part=2018-10
--2	checkout_date_part=2018-11
--3	checkout_date_part=2018-12
--4	checkout_date_part=2019-01
--5	checkout_date_part=2019-02