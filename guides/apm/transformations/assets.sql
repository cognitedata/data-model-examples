/* MAPPING_MODE_ENABLED: false */
/* {"version":1,"sourceType":"raw","mappings":[{"from":"externalId","to":"externalId","asType":"STRING"},{"from":"categoryId","to":"categoryId","asType":"INT"},{"from":"isCriticalLine","to":"isCriticalLine","asType":"BOOLEAN"},{"from":"sourceDb","to":"sourceDb","asType":"STRING"},{"from":"updatedDate","to":"updatedDate","asType":"TIMESTAMP"},{"from":"createdDate","to":"createdDate","asType":"TIMESTAMP"},{"from":"","to":"parent","asType":"STRUCT<`space`:STRING, `externalId`:STRING>"},{"from":"description","to":"description","asType":"STRING"},{"from":"tag","to":"tag","asType":"STRING"},{"from":"areaId","to":"areaId","asType":"INT"},{"from":"isActive","to":"isActive","asType":"BOOLEAN"}],"sourceLevel1":"oid","sourceLevel2":"cognite-oid-assets"} */
select
  cast(`externalId` as STRING) as externalId,
  cast(`categoryId` as INT) as categoryId,
  cast(`isCriticalLine` as BOOLEAN) as isCriticalLine,
  cast(`sourceDb` as STRING) as sourceDb,
  cast(`updatedDate` as TIMESTAMP) as updatedDate,
  cast(`createdDate` as TIMESTAMP) as createdDate,
  cast(`description` as STRING) as description,
  cast(`tag` as STRING) as tag,
  cast(`areaId` as INT) as areaId,
  cast(`isActive` as BOOLEAN) as isActive
from
  `oid`.`cognite-oid-assets`;