/* MAPPING_MODE_ENABLED: false */
/* {"version":1,"sourceType":"raw","mappings":[{"from":"externalId","to":"externalId","asType":"STRING"},{"from":"isCompleted","to":"isCompleted","asType":"BOOLEAN"},{"from":"plannedStart","to":"plannedStart","asType":"TIMESTAMP"},{"from":"isSafetyCritical","to":"isSafetyCritical","asType":"BOOLEAN"},{"from":"workPackageNumber","to":"workPackageNumber","asType":"STRING"},{"from":"endTime","to":"endTime","asType":"TIMESTAMP"},{"from":"status","to":"status","asType":"STRING"},{"from":"durationHours","to":"durationHours","asType":"INT"},{"from":"workOrderNumber","to":"workOrderNumber","asType":"STRING"},{"from":"title","to":"title","asType":"STRING"},{"from":"percentageProgress","to":"percentageProgress","asType":"INT"},{"from":"startTime","to":"startTime","asType":"TIMESTAMP"},{"from":"actualHours","to":"actualHours","asType":"INT"},{"from":"description","to":"description","asType":"STRING"},{"from":"isCancelled","to":"isCancelled","asType":"BOOLEAN"},{"from":"isActive","to":"isActive","asType":"BOOLEAN"},{"from":"priorityDescription","to":"priorityDescription","asType":"STRING"},{"from":"dueDate","to":"dueDate","asType":"TIMESTAMP"},{"from":"createdDate","to":"createdDate","asType":"TIMESTAMP"},{"from":"programNumber","to":"programNumber","asType":"STRING"}],"sourceLevel1":"{{cookiecutter.prefix}}{{cookiecutter.apm_simple_raw_db}}","sourceLevel2":"workorders"} */
select
  cast(`externalId` as STRING) as externalId,
  cast(`isCompleted` as BOOLEAN) as isCompleted,
  cast(`plannedStart` as TIMESTAMP) as plannedStart,
  cast(`isSafetyCritical` as BOOLEAN) as isSafetyCritical,
  cast(`workPackageNumber` as STRING) as workPackageNumber,
  cast(`endTime` / 1000 as TIMESTAMP) as endTime,
  cast(`status` as STRING) as status,
  cast(`durationHours` as INT) as durationHours,
  cast(`workOrderNumber` as STRING) as workOrderNumber,
  cast(`title` as STRING) as title,
  cast(`percentageProgress` as INT) as percentageProgress,
  cast(`startTime` / 1000 as TIMESTAMP) as startTime,
  cast(`actualHours` as INT) as actualHours,
  cast(`description` as STRING) as description,
  cast(`isCancelled` as BOOLEAN) as isCancelled,
  cast(`isActive` as BOOLEAN) as isActive,
  cast(`priorityDescription` as STRING) as priorityDescription,
  cast(`dueDate` as TIMESTAMP) as dueDate,
  cast(`createdDate` as TIMESTAMP) as createdDate,
  cast(`programNumber` as STRING) as programNumber
from
  `{{cookiecutter.prefix}}{{cookiecutter.apm_simple_raw_db}}`.`workorders`;