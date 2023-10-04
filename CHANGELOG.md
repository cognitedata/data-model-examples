# Changelog

**Please add new changelog items at the top!**

## Oct 4, 2023

- Add support for dumping and loading of all data models, views, containers, and spaces, also
  including global system models, views, and containers. `dump_datamodel all|global <model>|all <folder>`
  will dump from all (including global spaces) and either the model or all models. Also views and containers
  without a data model will be dumped. The dump will be structured with a directory per space.
- `load_data.py --load datamodeldump <example>` will load from examples/<example>/data_model/, including one level
  of subdirectories.
- Add support for cleaning out all data in a CDF project, CAREFUL!! `delete_data.py --delete datamodelall --instances --dry-run all` will delete all configuration in your project and clean out all instances. Use `--dry-run`
  to see what will happen. Drop the `--instances` to only delete the configuration and fail on deletion of spaces
  if there are remaining instances.

## Oct 2, 2023 - Adapt the repo to continuous testing

- Support use of env var CDF_TOKEN to supply OAuth2 token and thus not require
  OAuth2 client config. The token can also be supplied when instantiating CDFToolConfig.
- Add installable package data_model_examples.utils for dev and test purposed (not public).
- Add support for supplying OAuth2 token when instantiating CDFToolConfig.
- Add optional directory parameter to load and delete functions for direct
    loading and deletion of data from a directory.
- Upgrade to Cognite Python SDK 6.28.0
- Add new .environ(attr) method to CDFToolConfig to allow for easy loading of
    environment variables.
- Add new load_readwrite_group() function to load.py to support loading of
  groups with a set of capabilities (should not be used to manipulate admin group due to
  risk of loosing access).
- Add support for dumping and loading of transformations to/from JSON and SQL files without
  auth configuration (new dump_transformations.py scropt and dump_transformations() and
  load_transformations_dump() functions in utils).

## Sep 7, 2023

- Fix inconsistency in default naming of imports
- Fix bug in delete_datamodel() - not including ToolGlobals

## Aug 30, 2023

- Update timeseries datapoints to today

## Aug 24, 2023

- Factor out all functions into the utils/ module to make them easy to load from other scripts.
- Support and validate use of the utils/ module from JupyterLite notebooks in Fusion UI.

## Jul 7, 2023

- Add "audience" to the OAuth2 client config to support Auth0 without the default audience set.
- [BREAKING] Upgrade to Python 3.11 as 3.10 no longer has binary distributions.

## June 30, 2023

- Add direct loading of data model from load_data.py
- Add describe_datamodel.py <space> <data_mdodel> as a way to understand a data model
- Upgrade CDF Python SDK to 3.4.8
- Upgrade python-dotenv to 1.0.0
- Refactor delete_datamodel to use more specific queries
- Add --dry-run as option to delete_data.py

## June 12, 2023

- Made publicly available
