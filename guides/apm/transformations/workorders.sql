/* MAPPING_MODE_ENABLED: false */
/* {"version":1,"sourceType":"raw","mappings":[{"from":"externalId","to":"externalId","asType":"STRING"},{"from":"description","to":"description","asType":"STRING"},{"from":"endTime","to":"endTime","asType":"TIMESTAMP"},{"from":"WorkOrderStatus","to":"status","asType":"STRING"},{"from":"source","to":"sourceId","asType":"STRING"},{"from":"WorkOrderPriority","to":"priority","asType":"INT"},{"to":"startTime","asType":"TIMESTAMP","from":"startTime"},{"from":"WorkOrderTitle","to":"title","asType":"STRING"},{"from":"type","to":"type","asType":"STRING"}],"sourceLevel1":"apm_docs","sourceLevel2":"workorders"} */
select
  cast(`externalId` as STRING) as externalId,
  cast(`description` as STRING) as description,
  cast(`endTime`/1000 as TIMESTAMP) as endTime,
  cast(`WorkOrderStatus` as STRING) as status,
  cast(`source` as STRING) as sourceId,
  cast(`WorkOrderPriority` as INT) as priority,
  cast(`startTime`/1000 as TIMESTAMP) as startTime,
  cast(`WorkOrderTitle` as STRING) as title,
  cast(`type` as STRING) as type
from
  `apm_docs`.`workorders`;
  