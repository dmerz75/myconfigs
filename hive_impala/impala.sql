-- API:
invalidate metadata dd_media_in.grofers_purchasing_hist_test
refresh dd_media_in.grofers_purchasing_hist_test
compute stats dd_media_in.grofers_purchasing_hist_test
show table stats dd_media_in.grofers_purchasing_hist_test
describe formatted dd_media_in.grofers_purchasing_hist
select * from dd_media_in.grofers_purchasing_hist_test limit 20



-------------------------------BEGIN:
invalidate metadata dd_tv_media.nielsen_rld_type33_temp
refresh dd_tv_media.nielsen_rld_type33_temp


-- 18129
select count(1) from dd_tv_media.nielsen_rld_type33_temp
select * from dd_tv_media.nielsen_rld_type33_temp limit 20

-- Checks:
select distinct eastern_time_zone_date from dd_tv_media.nielsen_rld_type33_temp limit 50
select count(distinct eastern_time_zone_date) from dd_tv_media.nielsen_rld_type33_temp

-- 14267
select count(1)
from dd_tv_media.nielsen_rld_type33_temp
where trim(cast(eastern_time_zone_date as string)) != ""

-- 3862
select count(1)
from dd_tv_media.nielsen_rld_type33_temp
where trim(cast(eastern_time_zone_date as string)) is null
