# Cognite Data Fusion Data Model Examples

This repository contains examples on how to work with data models in Cognite Data Fusion.

## KNOWN ISSUES

* Once the data model has been populated with data using the transformations, the data in the data
    model must be manually deleted BEFORE deleting the data model. The load_datamodel.sh script
    will just try to create the data model. You can delete the data model without deleting the
    data, but be aware that the data will NOT be deleted if you delete the data model.

## Set up the CDF project and get credentials

**You need a CDF project and client credentials for a service account/principal that has access to the project
through a CDF access group (see below for needed permissions). You get the CDF project from
<support@cognite.com> and you configure the service principal/account in the identity provider (e.g. Azure Active Directory)
that the CDF project has been configured to use.**

See the python SDK [intro doc](https://docs.cognite.com/dev/guides/sdk/python/python_auth_oidc/) for how to get the credentials.
The minimum CDF credentials needed are (note that if you scope to data sets, you need to make sure you include ALL data sets for ALL
the examples you want to run or use the same data set for all examples):

* RAW: LIST, READ, WRITE either on all or scoped to the databases you configure for all examples
* dataSetsAcl: OWNER, READ, WRITE either on all or scoped to the data sets you configure for all examples
* dataModelsAcl: READ, WRITE either on all or scoped to the scopes you configure for all examples
* dataModelInstancesAcl: READ, WRITE either on all or scoped to the scopes you configure for all examples
* transformationsAcl: READ, WRITE either on all or scoped to the data sets you configure for all examples
* timeSeriesAcl: READ, WRITE either on all or scoped to the data sets you configure for all examples
* filesAcl: READ, WRITE either on all or scoped to the data sets you configure for all examples

## Getting Started by using cookiecutter

The easiest way to use this repo is not to check it out, but rather use cookiecutter to make a local copy:

```bash
pip install cookiecutter
cookiecutter https://github.com/cognitedata/data-model-examples.git
```

You will be prompted to supply your credentials for a CDF project (you need client credentials, so a client
id and a client secret).

The minimum you need to configure are the following (IDP = Identity Provider, typically Azure Active Directory):

* CDF_CLUSTER (the prefix before cognitedata.com)
* CDF_PROJECT (your CDF project name)
* IDP_TENANT_ID (the tenant id for the CDF project in your identity provider, for Azure this can be .something.onmicrosft.com)
* IDP_CLIENT_ID (the client id for the service principal/service account you have set up in your IDP)
* IDP_CLIENT_SECRET (the client secret for the service principal/service account you have set up in your IDP)

The remaining configurations are optional, but you will be prompted for them, so just press enter if you do not
need to change them.

**The prefix tells you were you get the information from: CDF_* is for your CDF project, while IDP_* is from your
identity provider.**

You will get a `./build` folder (unless you change the default) that contains the examples configured and ready
for your CDF project!

Cookiecutter will store your configurations in `~/.cookiecutter_replay/`, so you can update the build folder
by running `cookiecutter --replay https://github.com/cognitedata/data-model-examples.git`

## Prerequisites to run the examples

Each of the folders with examples have a README.md with more details, but you will need some prerequisites installed for all
examples.

1. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and
    [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) if you do not already have them.

2. Change directory into the `./build` folder

3. Install the data modeling cli tool:

    ```bash
    sudo npm install -g @cognite/cdf-cli
    ```

    Alternatively, run without `sudo` and add `~/.npm/bin` to your `PATH` environment variable.

4. Install the python requirements (or use poetry if you prefer that package manager):

    ```bash
    pip install -r requirements.txt
    ```

    or

    ```bash
    poetry install
    ```

5. Authenticate with the data modeling cli tool:

    ```bash
    ./cdf-login.sh
    ```

    This will try to log you into your CDF project with the credentials from the .env file. It will also try to list the transformations this
    client has access to.

    Note that the load_data.py script will test if it has correct permission and give you an error.

6. Load the environment variables from the .env file in the build folder:

    ```bash
    cd build
    set -a; source .env; set +a
    ```

    This is necessary for the python and bash scripts (including transformations-cli) to find the correct credentials.

7. To load the data set, use `load_data.py` script (if you use poetry, remember to run `poetry shell` first)

    Run `./load_data.py --help` to see the options.

    If you want to load all the data in the apm_simple data set, run:

    ```bash
    ./load_data.py --drop true apm_simple
    ```

    Adding `--drop true` will delete all the data that can be deleted before
    loading the data fresh. **Please note that data sets cannot be deleted!!**

8. Load the data model

    To load the data model for a specific example, run:

    ```bash
    ./<example_dir>/load_data_model.sh
    ```

9. Look at the README.md in each example folder. It will tell you if there are more example-specific options, like loading and running transformations etc.

## About the examples

This library of examples will be continouosly maintained and expanded.

### movie_actors

The movie_actors example contains csv raw data that are loaded into CDF RAW, a simple data model,
and transformations that will ingest data from the RAW database into the data model.

The example is simple to understand and the documentation can be found at <https://docs.cognite.com/cdf/data_modeling/guides/upload_demo_dm>.

### apm_simple

The apm_simple example is a more full-fledged data set with a data model that examplifies how to
store data within the Asset Performance Management space. The model itself is simplified and
should not be used for production purposes, but illustrates some key principles.

In addition to raw csv data, transformations, and a data modle, this data set also contains
a select few time series from a compressor at Valhall from the North Sea. Also, a set of
Process and Instrumentation Diagrams (P&IDs) are included.

This makes this example more suitable for testing out the wider set of CDF functionalities, like
Charts for timeseries investigations and plotting.

See [Open Industrial Data](https://hub.cognite.com/open-industrial-data-211/what-is-open-industrial-data-994) for more information.

## About this template repository

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to contribute to the templates or new examples.
