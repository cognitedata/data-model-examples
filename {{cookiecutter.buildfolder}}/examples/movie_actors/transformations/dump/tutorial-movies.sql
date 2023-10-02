/* MAPPING_MODE_ENABLED: true */
/* {"version":1,"sourceType":"raw","mappings":[ {"from":"Movie_Name","to":"externalId","asType":"STRING"}, {"from":"Movie_Name","to":"name","asType":"STRING"}, {"from":"Description","to":"description","asType":"STRING"}, {"from":"Run_time","to":"runTime","asType":"INT"}, {"from":"Gross_USD","to":"gross","asType":"INT"}, {"from":"Director","to":"director","asType":"STRUCT<STRING:STRING>"}, {"from":"IMDB_Rating","to":"imdbRating","asType":"DOUBLE"}, {"from":"Released_Year","to":"releasedYear","asType":"INT"}, {"from":"","to":"watchedIt"}], "sourceLevel1":"tutorial_movies","sourceLevel2":"movies"} */
select
  cast(`id` as STRING) as externalId,
  cast(`Movie_Name` as STRING) as name,
  cast(`Description` as STRING) as description,
  cast(`Run_time` as INT) as runTime,
  cast(`Gross_USD` as INT) as gross,
  node_reference('tutorial_movies', Director) as director,
  cast(`IMDB_Rating` as DOUBLE) as imdbRating,
  cast(`Released_Year` as INT) as releasedYear
from
  `tutorial_movies`.`movies`;
