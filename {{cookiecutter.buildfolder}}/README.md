# Cognite Data Fusion Data Model Examples

These examples are examples of how to work with data models and data sets in Cognite Data Fusion.

The code is licensed under the [Apache License 2.0](LICENSE.code.md), while the documentation and methods are licensed
under [Creative Commons](LICENSE.docs.md). Each of the example data sets has its own license, see the LICENSE.dataset.md in each
directory.

## KNOWN ISSUES

* N/A

## Set up the CDF project and get credentials

**You need a CDF project and client credentials for a service account/principal that has access to the project
through a CDF access group (see below for needed permissions). You get the CDF project from
<support@cognite.com> and you configure the service principal/account in the identity provider (e.g. Azure Active Directory)
that the CDF project has been configured to use.**

See the Python SDK [intro doc](https://developer.cognite.com/dev/guides/sdk/python/python_auth_oidc/) for how to get the credentials.
The minimum CDF credentials needed are (note that if you scope to data sets, you need to make sure you include ALL data sets for ALL
the examples you want to run or use the same data set for all examples):

* RAW: LIST, READ, WRITE either on all or scoped to the databases you configure for all examples
* dataSetsAcl: OWNER, READ, WRITE either on all or scoped to the data sets you configure for all examples
* dataModelsAcl: READ, WRITE either on all or scoped to the scopes you configure for all examples
* dataModelInstancesAcl: READ, WRITE either on all or scoped to the scopes you configure for all examples
* transformationsAcl: READ, WRITE either on all or scoped to the data sets you configure for all examples
* timeSeriesAcl: READ, WRITE either on all or scoped to the data sets you configure for all examples
* filesAcl: READ, WRITE either on all or scoped to the data sets you configure for all examples

## Prerequisites to run the examples

Each of the folders with examples has a README.md with more details, but you will need some prerequisites installed for all
examples.

1. Install Python and [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/)
    if you do not already have them.

1. Change directory into the `./build` folder

1. Install the Python requirements (or use poetry if you prefer that package manager):

    ```bash
    pip install -r requirements.txt
    ```

    or

    ```bash
    poetry install
    ```

## Load the data

**Once you have installed pre-requisites, you can do the super-fast bootstrap of the dataset by running:**

```bash
./clean_and_load.sh <example>
```

This script will drop all data (if present), re-load everything, and then run the transformations to
get data into your data model.

Or, you can do the steps one by one (you can also look at the `./clean_and_load.sh` script):

1. Load the environment variables from the .env file in the build folder:

    ```bash
    cd build
    set -a; source .env; set +a
    ```

    This is necessary for the Python scripts (also transformations-cli tool if you use it) to find the correct credentials.

1. To load the data set, use `load_data.py` script (if you use poetry, remember to run `poetry shell` first)

    Run `./load_data.py --help` to see the options.

    If you want to load all the data in the apm_simple data set, run:

    ```bash
    ./load_data.py --drop apm_simple
    ```

    Adding `--drop` will delete all the data that can be deleted before
    loading the data fresh. **Please note that CDF datasets cannot be deleted, they will be empty after a delete!!**

    *This command will also default load the transformations in the example directory. You can also use the transformations-cli tool to load the transformations (and more). The environment variables needed for transformations are already set.*

1. Run the transformations

    To run the transformations for a specific example, run:

    ```bash
    ./run_transformations.py <example_dir>
    ```

    This will run all the transformations in the example folder. If you want to run a specific
    transformation, you can specify `--file name-of-transformation.yaml` as an option.

1. Look at the README.md in each `./example/*` folder. It will tell you if there are more example-specific options.

## About the examples

This library of examples will be continuously maintained and expanded.

### movie_actors

The movie_actors example contains CSV raw data that are loaded into CDF RAW, a simple data model,
and transformations that will ingest data from the RAW database into the data model.

The example is simple to understand and the documentation can be found at: <https://docs.cognite.com/cdf/data_modeling/guides/upload_demo_dm>.

### apm_simple

The apm_simple example is a more full-fledged data set with a data model that exemplifies how to
store data within the Asset Performance Management space. The model itself is simplified and
should not be used for production purposes, but illustrates some key principles.

In addition to raw CSV data, transformations, and a data model, this data set also contains
a select few time series from a compressor at Valhall from the North Sea. Also, a set of
Process and Instrumentation Diagrams (P&IDs) are included.

This makes this example more suitable for testing out the wider set of CDF functionalities, like
Charts for timeseries investigations and plotting.

See [./examples/apm_simple/README.md](./examples/apm_simple/README.md) for more information.

### Data Modeling CLI tool

You can install the cdf-cli tool for data models from npm:

```bash
sudo npm install -g @cognite/cdf-cli
```

Alternatively, run without `sudo` and add `~/.npm/bin` to your `PATH` environment variable.

You can then log into the tool:

```bash
set -a 
source ./.env
set +a
echo "Logging into CDF using environment variables from .env..."
cdf login --client-id=$IDP_CLIENT_ID --client-secret=$IDP_CLIENT_SECRET --tenant=$IDP_TENANT_ID --cluster=$CDF_CLUSTER $CDF_PROJECT
cdf status
```

And then load the data model:

```bash
cdf dm create --interactive false --external-id data_model_name --space space_name data_model_name
cdf dm publish --interactive false --external-id data_model_name --space space_name --version 1 --file ./examples/<example>/datamodel.graphql
```

## Structure of each example

In the `./examples` directory, you will find the following:

* `LICENSE.dataset.md`: The license for the data set.
* `README.md`: More details about the data set.
* `requirements.txt/pyproject.toml`: if there are any additional requirements for using the data set (not
    for loading the data set, that is handled by the `requirements.txt` in the build folder).
* `data/` directory with files, raw, and timeseries that are loaded by load_data.py.
* `transformations/` directory with transformations definitions (YAML files) that are loaded by
    load_data.py.
* `data_model/` directory with data model definitions (json files) that are loaded by load_data.py
    using the Python SDK (and the /model/ REST APIs).
* `datamodel.graphql`: the graphql schema for the data model that you can load info CDF from the
    CDF UI. This schema file can also be used by the CDF CLI tool for data models (see below).

## describe_datamodel.py

The `describe_datamodel.py <space> <data_model>` script will describe any data model (no writing happens) and
can be used on your own data models as well (not only the examples).

An example for the apm_simple model can be seen below.

```txt
Describing data model ({model_name}) in space ({space_name})...
Verifying access rights...
Found the space tutorial_apm_simple with name (None) and description (None).
  - created_time: 2023-06-29 10:41:41.282000
  - last_updated_time: 2023-06-29 10:41:46.139000
Found 3 containers in the space tutorial_apm_simple:
  Asset
  WorkItem
  WorkOrder
Found data model tutorial_apm_simple in space tutorial_apm_simple:
  version: 1
  global: False
  description: None
  created_time: 2023-06-29 10:41:41.963000
  last_updated_time: 2023-06-29 10:41:47.444000
  tutorial_apm_simple has 3 views:
    Asset, version: aea363cc6d37ba
       - properties: 11
       - used for nodes
       - implements: None
       - direct relation 1:1 parent --> (tutorial_apm_simple, Asset, aea363cc6d37ba)
       - edge relation 1:MANY children -- outwards --> (tutorial_apm_simple, Asset, aea363cc6d37ba)
    WorkOrder, version: 5f8749a07c2940
       - properties: 21
       - used for nodes
       - implements: None
       - edge relation 1:MANY workItems -- outwards --> (tutorial_apm_simple, WorkItem, f9c8dbdc9ddb2d)
       - edge relation 1:MANY linkedAssets -- outwards --> (tutorial_apm_simple, Asset, aea363cc6d37ba)
    WorkItem, version: f9c8dbdc9ddb2d
       - properties: 10
       - used for nodes
       - implements: None
       - direct relation 1:1 workOrder --> (tutorial_apm_simple, WorkOrder, 5f8749a07c2940)
       - edge relation 1:MANY linkedAssets -- outwards --> (tutorial_apm_simple, Asset, aea363cc6d37ba)
Total direct relations: 2
Total edge relations: 4
------------------------------------------
Found in total 15628 edges in space tutorial_apm_simple spread over 4 types:
  WorkOrder.workItems: 1536
  WorkItem.linkedAssets: 6494
  WorkOrder.linkedAssets: 6493
  Asset.children: 1105
------------------------------------------
Found in total 3961 nodes in space tutorial_apm_simple across all views and containers.
  1105 nodes of view Asset.
  1314 nodes of view WorkOrder.
  1536 nodes of view WorkItem.
```
