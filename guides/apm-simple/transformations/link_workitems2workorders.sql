/* MAPPING_MODE_ENABLED: true */
/* {"version":1,"sourceType":"raw","mappings":[{"from":"externalId","to":"externalId","asType":"STRING"},{"from":"sourceExternalId","to":"startNode","asType":"STRUCT<`space`:STRING, `externalId`:STRING>"},{"from":"targetExternalId","to":"endNode","asType":"STRUCT<`space`:STRING, `externalId`:STRING>"}],"sourceLevel1":"oid","sourceLevel2":"workorder2items"} */
select
  cast(`externalId` as STRING) as externalId,
  node_reference('apm_docs', `sourceExternalId`) as startNode,
  node_reference('apm_docs', `targetExternalId`) as endNode
from
  `oid`.`workorder2items`;