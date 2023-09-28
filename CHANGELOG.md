# Changelog

**Please add new changelog items at the top!**

## Sep XX, 2023 - Adapt the repo to continuous testing

- Add installable package data_model_examples.utils
- Add support for supplying OAuth2 token with instantiating CDFToolConfig

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
