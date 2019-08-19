
-- Table modifications:
drop table dd_media_in.grofers_event
alter table dd_media_in.grofers_event RENAME TO dd_media_in.grofers_event1
select count(*) from dd_media_in.grofers_purchasing_hist9
SELECT * FROM grofers_purchasing_hist10 LIMIT 20;
describe formatted dd_media_in.grofers_purchasing_hist
-- End of Table modifications.

-- Straight from parquet to hive!
--Step 1.
CREATE EXTERNAL TABLE IF NOT EXISTS dd_media_in.grofers_event (`customer_id` BIGINT,
`product_id` DOUBLE,`event_name` STRING,`product_list_name` STRING,`session_id` STRING,
`event_time` STRING)
STORED AS PARQUET
LOCATION '/enterprise_data/dev/media_in/grofers/raw/event_round4/'

--ROW FORMAT DELIMITED
--FIELDS TERMINATED BY '|'

--Step 2.
-- LOAD RAW DATA:
load data inpath   '/enterprise_data/dev/tv_media/rld/type72_unfiltered'
into table dd_tv_media.type72_unfiltered
-- End of parquet to hive.

