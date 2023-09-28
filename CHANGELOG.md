# Changelog

**Please add new changelog items at the top!**

## Sep 28, 2023 - Adapt the repo to continuous testing

- Support use of env var CDF_TOKEN to supply OAuth2 token and thus not require
  OAuth2 client config. The token can also be supplied when instantiating CDFToolConfig.
- Add installable package data_model_examples.utils for dev and test purposed (not public).
- Add support for supplying OAuth2 token with instantiating CDFToolConfig.
- Add optional directory parameter to load and delete functions for direct
    loading and deletion of data from a directory.
- Upgrade to Cognite Python SDK 6.28.0
- Add new .environ(attr) method to CDFToolConfig to allow for loading of
    environment variables.
- Add new load_readwrite_group() function to load.py to support loading of
  groups with a set of capabilities (should not be used to manipulate admin group).

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
