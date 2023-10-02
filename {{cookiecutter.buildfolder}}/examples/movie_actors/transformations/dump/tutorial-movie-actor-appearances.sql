/* MAPPING_MODE_ENABLED: true */
/* {"version":1,"sourceType":"raw","mappings":[ {"from":"id","to":"externalId","asType":"STRING"}, {"from":"movie","to":"startNode","asType":"STRUCT<STRING:STRING>"}, {"from":"actor","to":"endNode","asType":"STRUCT<STRING:STRING>"}], "sourceLevel1":"tutorial_movies","sourceLevel2":"actor_movie_appearances"} */
select
  cast(`id` as STRING) as externalId,
  node_reference('tutorial_movies', movie) as startNode,
  node_reference('tutorial_movies', actor) as endNode
from
  `tutorial_movies`.`actor_movie_appearances`;
