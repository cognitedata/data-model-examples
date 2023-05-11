/* MAPPING_MODE_ENABLED: true */
/* {"version":1,"sourceType":"raw","mappings":[{"from":"externalId","to":"externalId","asType":"STRING"},{"from":"sourceExternalId","to":"startNode","asType":"STRUCT<`space`:STRING, `externalId`:STRING>"},{"to":"endNode","asType":"STRUCT<`space`:STRING, `externalId`:STRING>","from":"targetExternalId"}],"sourceLevel1":"{{cookiecutter.prefix}}{{cookiecutter.apm_simple_raw_db}}","sourceLevel2":"workorder2assets"} */
select
  cast(`externalId` as STRING) as externalId,
  node_reference('{{cookiecutter.apm_simple_space}}', `sourceExternalId`) as startNode,
  node_reference('{{cookiecutter.apm_simple_space}}', `targetExternalId`) as endNode
from
  `{{cookiecutter.prefix}}{{cookiecutter.apm_simple_raw_db}}`.`workorder2assets`;