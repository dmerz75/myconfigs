-- hive_dynamic_partitioning_from_1_parquet.sql

--These are the steps to go from uploading 1 parquet file onto hdfs to
--registering a dynamically partitioned hive table.

-- A nice blog:
-- https://medium.com/a-muggles-pensieve/writing-into-dynamic-partitions-using-spark-2e2b818a007a

table: event_r9
data: event_r13
ptable: event_p13

-- EVENT PARTITIONING:
-- 1. Create the unpartitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_event_r9
(`customer_id` INT, `event_time` STRING, `product_id` INT,
 `event_name` STRING,`product_list_name` STRING,`session_id` STRING,
  event_date STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/event_r13/'

-- 2. Load data into the unpartitioned table.
load data inpath '/enterprise_data/dev/media_in/grofers/raw/event_r13'
into table dd_media_in.grofers_purchasing_hist_r9

-- 3. Confirm the total count. (502353705)
select count(1) from dd_media_in.grofers_event_r9

-- 4. Set the dynamic partitioning configurations.
SET hive.exec.dynamic.partition = true
SET hive.exec.dynamic.partition.mode = nonstrict

-- 5. Create the partitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_event_p8
(`customer_id` INT, `event_time` STRING, `product_id` INT,
 `event_name` STRING,`product_list_name` STRING,`session_id` STRING)
PARTITIONED BY (checkout STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/event_r13'

-- 6. Insert the unpartitioned data into the partitioned table.
INSERT OVERWRITE TABLE dd_media_in.grofers_event_p8
PARTITION(checkout_date_part)
SELECT * FROM dd_media_in.grofers_event_r9

-- 7. Confirm the partitions in the partitioned table.
show partitions dd_media_in.grofers_event_p8

-- 8. Confirm the total count, unpartitioned vs partitioned table.
select count(1) from dd_media_in.grofers_event_p8

-- 9. Some final organization commands.
ALTER VIEW dd_media_in.grofers_purchasing_hist RENAME TO dd_media_in.grofers_event_v1

CREATE VIEW IF NOT EXISTS grofers_purchasing_hist AS SELECT * FROM grofers_event_p8

desc dd_media_in.grofers_event_p8

show partitions dd_media_in.grofers_event_p8
--1 checkout_date_part=2018-10
--2	checkout_date_part=2018-11
--3	checkout_date_part=2018-12
--4	checkout_date_part=2019-01
--5	checkout_date_part=2019-02



--- WORKING
drop table dd_media_in.grofers_event_r9

-- EVENT PARTITIONING:
-- 1. Create the unpartitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_event_r9 (`customer_id` INT,
`event_time` STRING, `product_id` INT, searched_keyword STRING, `event_name` STRING,
`product_list_name` STRING,`session_id` STRING, `event_date` STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/event_r13/'


-- 2. Load data into the unpartitioned table.
load data inpath '/enterprise_data/dev/media_in/grofers/raw/event_r13'
into table dd_media_in.grofers_event_r9

-- 3. Confirm the total count. (37095180)
select count(1) from dd_media_in.grofers_event_r9

-- 4. Set the dynamic partitioning configurations.
SET hive.exec.dynamic.partition = true
SET hive.exec.dynamic.partition.mode = nonstrict

drop table dd_media_in.grofers_event_p8

-- 5. Create the partitioned table.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_event_p8
(`customer_id` INT, `event_time` STRING, `product_id` INT, searched_keyword STRING, `event_name` STRING,
`product_list_name` STRING,`session_id` STRING)
PARTITIONED BY (event_date STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/event_r13'

-- 6. Insert the unpartitioned data into the partitioned table.
INSERT OVERWRITE TABLE dd_media_in.grofers_event_p8
PARTITION(event_date)
SELECT * FROM dd_media_in.grofers_event_r9

-- 7. Confirm the partitions in the partitioned table.
show partitions dd_media_in.grofers_event_p8

-- 8. Confirm the total count, unpartitioned vs partitioned table.
select count(1) from dd_media_in.grofers_event_p8

-- 9. Some final organization commands.
ALTER VIEW dd_media_in.grofers_event RENAME TO dd_media_in.grofers_event_v1

CREATE VIEW IF NOT EXISTS dd_media_in.grofers_event AS SELECT * FROM grofers_event_p8

desc dd_media_in.grofers_event_p8

show partitions dd_media_in.grofers_event
