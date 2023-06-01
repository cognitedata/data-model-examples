# APM Simple Example

## Load the transformations

When you have loaded the dataset and the data model as described in the main README.me, you can load the transformations.

```bash
cd ./build/apm_simple
transformations-cli deploy transformations
```

The transformations-cli tool will deploy all the .yaml configurations in the
transformations folder.

## Run the transformations

You can now run the transformations that will ingest the data from the RAW database into the Asset Performance Management data model:

```bash
./apm_simple/run_transformations.sh
```

## Investigation into operational states of a compressor

**NOTE!!! This notebook example is not yet simplified for access to credentials etc, so it requires a bit more knowledge to run. It is adapted to
run in an early preview of Jypiter notebooks run in your browser within Fusion.**

The jupyter notebook will show you how to query the data model using the Cognite Python SDK. The time series loaded in the data set are used to explore
various modes of operation for a compressor on Valhall.

See `Valhall Operational States 2.ipynb`.

## Use Charts

You can also use the Charts application to explore the data. Search for time series and add them to your chart.
