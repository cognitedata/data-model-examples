/* MAPPING_MODE_ENABLED: false */
/* {"version":1,"sourceType":"raw","mappings":[{"from":"externalId","to":"externalId","asType":"STRING"},{"from":"sourceExternalId","to":"startNode","asType":"STRUCT<`space`:STRING, `externalId`:STRING>"},{"to":"endNode","asType":"STRUCT<`space`:STRING, `externalId`:STRING>","from":"targetExternalId"}],"sourceLevel1":"oid","sourceLevel2":"cognite-oid-workorder2assets"} */
select
  cast(`externalId` as STRING) as externalId,
  node_reference('apm_docs', `sourceExternalId`) as startNode,
  node_reference('apm_docs', `targetExternalId`) as endNode
from
  `oid`.`cognite-oid-workorder2assets`;