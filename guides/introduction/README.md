# Introduction to data modeling
This is the reference code for the [introduction to data modeling](https://docs.cognite.com/cdf/data_modeling/intro_to_dm) in documentation. This tutorial assumes you have access to execute Python (and install packages using `pip`) and install packages using `npm` through the terminal.

In this tutorial, we only create, deploy and populate the data model. See [Query data from a data model](https://docs.cognite.com/cdf/data_modeling/guides/query_data_dm) on how to query the data.

## Prerequisites
1. [Upload the demo data to RAW](https://docs.cognite.com/cdf/data_modeling/upload_raw_dm)
1. Install the CDF transformations cli tool `pip install cognite-transformations-cli`
1. Install the CDF cli tool `npm install -g @cognite/cdf-cli`
1. Authenticate with CLI tool `cdf signin <project>`

## Create and upload the data model
First we need to create the data model
    ```
    cdf dm create Movie --external-id Movie --space Movie
    ```
This will create an empty data model you can then see in Fusion. Then we upload the data model with
    ```
    cdf dm publish --external-id Movie --space Movie --file datamodel.graphql --version 1
    ```
You can now go to Fusion to see the data model. The next step is to populate the data model. We show how you can do that in two different ways. One is using CDF transformations moving data from RAW into your data model, and the other is using the data modeling API directly through Python. We begin with the CDF transformations.

## Populate data model using CDF transformations
### Upload data to RAW
First, we need to upload the CSV files containing the data found in the [data](data) folder. We can do that either by going to Fusion and uploading it to RAW using the UI, or upload it using Python. The latter is not covered by this tutorial. To upload using the UI, follow [this guide](https://docs.cognite.com/cdf/data_modeling/upload_raw_dm).

### Create CDF transformations
In the [transformations](transformations) folder you will find a set for transformations configuration files (yaml-files) that can be deployed using the transformations CLI tool. These transformations may run on a schedule and thus requires [client credentials](https://docs.cognite.com/cdf/integration/guides/transformation/admin_oidc), grab those first. You also need some other OIDC values. Check [../load_credentials.sh](../load_credentials.sh) to see which ones, and paste them in there.

Then, we load these credentials with
    ```
    source ../load_credentials.sh
    ```
before we can deploy the transformations with
    ```
    transformations-cli deploy transformations
    ```
They should now be deployed and ready for execution. Now we run each one by these commands
    ```
    transformations-cli run --external-id tutorial-actors
    transformations-cli run --external-id tutorial-directors
    transformations-cli run --external-id tutorial-movies
    transformations-cli run --external-id tutorial-movie-actor-appearances
    ```
Go to [Query data from a data model](https://docs.cognite.com/cdf/data_modeling/guides/query_data_dm) to see how you can query the data in this data model.