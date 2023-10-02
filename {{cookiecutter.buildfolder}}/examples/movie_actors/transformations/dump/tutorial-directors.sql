/* MAPPING_MODE_ENABLED: true */
/* {"version":1,"sourceType":"raw","mappings":[ {"from":"name","to":"externalId","asType":"STRING"}, {"from":"name","to":"name","asType":"STRING"}, {"to":"age","asType":"INT"},{"from":"","to":"didWinOscar"}], "sourceLevel1":"tutorial_movies","sourceLevel2":"directors"} */
select
  cast(`name` as STRING) as externalId,
  cast(`name` as STRING) as name
from
  `tutorial_movies`.`directors`;
