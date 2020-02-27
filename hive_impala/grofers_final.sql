
-- CREATE DYNAMIC PARTITIONING
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;


-- DROP TABLE
drop table dd_media_in.grofers_demographic_r7
drop table dd_media_in.grofers_event_r9
drop table dd_media_in.grofers_purchasing_hist_r7
drop table dd_media_in.grofers_flipkart_r8


-- DROP VIEW
drop view dd_media_in.grofers_purchasing_hist_r2
drop view dd_media_in.grofers_purchasing_hist_r3
drop view dd_media_in.grofers_event_v1
drop view dd_media_in.grofers_demographic
drop view dd_media_in.grofers_purchasing_hist_v1
drop view dd_media_in.grofers_flipkart


-- CREATE VIEW:
CREATE VIEW IF NOT EXISTS grofers_purchasing_hist AS SELECT * FROM grofers_purchasing_hist_r8
CREATE VIEW IF NOT EXISTS grofers_demographic AS SELECT * FROM grofers_demographic_r12
CREATE VIEW IF NOT EXISTS grofers_event AS SELECT * FROM grofers_event_r8
CREATE VIEW IF NOT EXISTS grofers_flipkart AS SELECT * FROM grofers_flipkart_r0

drop view grofers_demographic

-- ALTER/CHANGE TABLE NAME
alter table dd_media_in.grofers_purchasing_hist RENAME TO dd_media_in.grofers_purchasing_hist_r6
alter table dd_media_in.grofers_demographic RENAME TO dd_media_in.grofers_demographic_r6
alter table dd_media_in.grofers_event RENAME TO dd_media_in.grofers_event_r6

describe formatted dd_media_in.grofers_purchasing_hist


-- COUNT:
select count(1) from dd_media_in.grofers_demographic_r12
select count(1) from dd_media_in.grofers_event_r8
select count(1) from dd_media_in.grofers_purchasing_hist
select count(1) from dd_media_in.grofers_purchasing_hist_p8
select count(1) from dd_media_in.grofers_flipkart


-- VIEW:
select * from dd_media_in.grofers_purchasing_hist_r7 limit 20
select * from dd_media_in.grofers_demographic_r11 limit 20
select * from dd_media_in.grofers_event_r7 limit 20
select * from dd_media_in.grofers_flipkart limit 20
select * from dd_media_in.flipkart limit 20


-- DESCRIBE:
-- /enterprise_data/dev/media_in/grofers/raw/purchase_hist_pqt
-- /enterprise_data/dev/media_in/grofers/raw/demographic
-- /enterprise_data/dev/media_in/grofers/raw/event
describe formatted dd_media_in.grofers_demographic
describe formatted dd_media_in.grofers_purchasing_hist
describe formatted dd_media_in.grofers_event

-- SHOW CREATE TABLE:
show create table grofers_event_r4

-- CREATE TABLE OUTPUT:
-- hdfs://hanameservice/enterprise_data/dev/media_in/grofers/raw/event_round4
-- 1	CREATE EXTERNAL TABLE `grofers_event_r4`(
-- 2	  `customer_id` bigint,
-- 3	  `product_id` double,
-- 4	  `event_name` string,
-- 5	  `product_list_name` string,
-- 6	  `session_id` string,
-- 7	  `event_time` string)
-- 8	ROW FORMAT SERDE
-- 9	  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
-- 10	STORED AS INPUTFORMAT
-- 11	  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat'
-- 12	OUTPUTFORMAT
-- 13	  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
-- 14	LOCATION
-- 15	  'hdfs://hanameservice/enterprise_data/dev/media_in/grofers/raw/event_round4'


-- LOADING SECTION ---:

-- 4-1. Flipkart
-- `index` INT,
--  `revenue_fsp` INT,
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_flipkart_r1 (
`approved_date` STRING, `date` STRING,
`account_id` STRING, `demographic_gender` STRING, `gender_behavior` STRING,
`is_married_flag` STRING, `age_bucket` STRING, `is_parent_flag` STRING,
`pincode` INT, `analytic_vertical` STRING, `units` INT, `totalorders` INT,
`gmv` DOUBLE, `fsp` DOUBLE, `mrp` DOUBLE,
`brand_id_final` STRING, `fsn_id_final` STRING,
`png_fsn` INT, `product_title_up` STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/flipkart_r1'

-- 4-2. Load data
load data inpath '/enterprise_data/dev/media_in/grofers/raw/flipkart_r1'
into table dd_media_in.grofers_flipkart_r1





-- DEMOGRAPHIC:
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_demographic_r12 (
    `customer_id` BIGINT,
    `churn_score` DOUBLE,
    `is_loyal` BOOLEAN,
    `file_date` STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/demographic_r16'

load data inpath '/enterprise_data/dev/media_in/grofers/raw/demographic_r16'
into table dd_media_in.grofers_demographic_r12

--    `__index_level_0__` BIGINT)
-- |-- customer_id: integer (nullable = true)
-- |-- churn_score: double (nullable = true)
-- |-- is_loyal: boolean (nullable = true)



-- PURCHASE_HIST PARTITIONING
-- 1. Create the unpartitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_purchasing_hist_r20
( `checkout_date` STRING, `merchant_id` BIGINT,`customer_id` BIGINT,`product_id` BIGINT,
  `product_name` STRING, `brand` STRING,`l_cat` STRING,`l1_cat` STRING,`l2_cat` STRING,
  `type_id` BIGINT, `type_name` STRING,`quantity` BIGINT,`price_mrp` DOUBLE,`order_id` BIGINT,
  checkout_date_part STRING )
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/purchase_hist_r20'
--
DROP TABLE dd_media_in.grofers_purchasing_hist_r20

-- 2. Load data into the unpartitioned table.
load data inpath '/enterprise_data/dev/media_in/grofers/raw/purchase_hist_r20'
into table dd_media_in.grofers_purchasing_hist_r20

-- 3. Confirm the total count. (37095180)
select count(1) from dd_media_in.grofers_purchasing_hist_r20

-- 4. Set the dynamic partitioning configurations.
SET hive.exec.dynamic.partition = true
SET hive.exec.dynamic.partition.mode = nonstrict

-- 5. Create the partitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_purchasing_hist_p20 (
    `checkout_date` STRING, `merchant_id` BIGINT,`customer_id` BIGINT,`product_id` BIGINT,
    `product_name` STRING,`brand` STRING,`l_cat` STRING,`l1_cat` STRING,`l2_cat` STRING,
    `type_id` BIGINT,`type_name` STRING,`quantity` BIGINT,`price_mrp` DOUBLE,`order_id` BIGINT
    )
PARTITIONED BY (checkout_date_part STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/purchase_hist_p20'

-- 6. Insert the unpartitioned data into the partitioned table.
INSERT OVERWRITE TABLE dd_media_in.grofers_purchasing_hist_p20
PARTITION(checkout_date_part)
SELECT * FROM dd_media_in.grofers_purchasing_hist_r20

-- 7. Confirm the partitions in the partitioned table.
show partitions dd_media_in.grofers_purchasing_hist_p20

-- 8. Confirm the total count, unpartitioned vs partitioned table.
select count(1) from dd_media_in.grofers_purchasing_hist_p20

-- 9. Some final organization commands.
DROP VIEW dd_media_in.grofers_purchasing_hist

CREATE VIEW IF NOT EXISTS grofers_purchasing_hist AS SELECT * FROM grofers_purchasing_hist_p20

ALTER VIEW dd_media_in.grofers_purchasing_hist RENAME TO dd_media_in.grofers_purchasing_hist_v1


desc dd_media_in.grofers_purchasing_hist_p11

show partitions dd_media_in.grofers_purchasing_hist_p11
--1 checkout_date_part=2018-10
--2	checkout_date_part=2018-11
--3	checkout_date_part=2018-12
--4	checkout_date_part=2019-01
--5	checkout_date_part=2019-02

-- PURCHASE CHECKS
select distinct * from dd_media_in.grofers_purchasing_hist
where merchant_id = 26049 and type_name = 'Basmati Rice'
-- order by event_time;
-- 60 rows, yes..

select  * from dd_media_in.grofers_purchasing_hist
where merchant_id = 26049 and type_name = 'Basmati Rice'
-- order by event_time;
-- 268 rows, yes..


-- EVENT PARTITIONING:
-- 1. Create the unpartitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_event_r11 (`customer_id` INT,
`event_time` STRING, `product_id` INT, searched_keyword STRING, `event_name` STRING,
`product_list_name` STRING,`session_id` STRING, `event_date` STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/event/r5/'
-- location is storage destination
DROP TABLE dd_media_in.grofers_event_r11

-- 2. Load data into the unpartitioned table.
load data inpath '/enterprise_data/dev/media_in/grofers/raw/event/r5/'
into table dd_media_in.grofers_event_r11


-- 3. Confirm the total count.
select count(1) from dd_media_in.grofers_event_r11


-- 4. Set the dynamic partitioning configurations.
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;
-- SET hive.auto.convert.join=false;
-- SET hive.exec.compress.output=false;
-- SET hive.exec.orc.default.compress=snappy;


-- 5. Create the partitioned table.
-- DROP TABLE dd_media_in.grofers_event_p11
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_event_p21
(`customer_id` INT, `event_time` STRING, `product_id` INT, searched_keyword STRING, `event_name` STRING,
`product_list_name` STRING,`session_id` STRING)
PARTITIONED BY (event_date STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/event_p21'

-- 6. Insert the unpartitioned data into the partitioned table.
-- overwrite -
INSERT OVERWRITE TABLE dd_media_in.grofers_event_p21
PARTITION(event_date)
SELECT * FROM dd_media_in.grofers_event_r11

-- -- DON'T USE
-- -- append -- resulted in 5 duplicates
-- INSERT INTO TABLE dd_media_in.grofers_event_p11
-- PARTITION(event_date)
-- SELECT * FROM dd_media_in.grofers_event_r5


-- 7. Confirm the partitions in the partitioned table.
show partitions dd_media_in.grofers_event_p21

-- 8. Some final organization commands.
DROP view dd_media_in.grofers_event
CREATE VIEW IF NOT EXISTS dd_media_in.grofers_event AS SELECT * FROM grofers_event_p21

-- 9. Confirm the total count, unpartitioned vs partitioned table.
select count(1) from dd_media_in.grofers_event_p21
select count(1) from dd_media_in.grofers_event

ALTER VIEW dd_media_in.grofers_event RENAME TO dd_media_in.grofers_event_v1

DESC dd_media_in.grofers_event

SHOW PARTITIONS dd_media_in.grofers_event


-- EVENT CHECKS:
select distinct * from dd_media_in.grofers_event
where customer_id = 9378232 and product_list_name = 'Diapers'
order by event_time;
-- 60 rows, yes..

select  * from dd_media_in.grofers_event
where customer_id = 9378232 and product_list_name = 'Diapers'
order by event_time;
-- 268 rows, yes..
