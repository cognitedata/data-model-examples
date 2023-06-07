# Asset Performance Management Simple Example

## About the data

This data is from [Open Industrial Data](https://hub.cognite.com/open-industrial-data-211/what-is-open-industrial-data-994).

Below is a snippet from the Cognite Hub website describing the data:

> The data originates from a single compressor on Aker BP’s Valhall oil platform in the North Sea. Aker BP selected the first stage compressor on the Valhall because it is a subsystem with
> clearly defined boundaries, rich in time series and maintenance data.
>
> AkerBP uses Cognite Data Fusion to organize the data stream from this compressor. The data set available in Cognite Data Fusion includes time series data, maintenance history, and
> Process & Instrumentation Diagrams (P&IDs) for Valhall’s first stage compressor and associated process equipment: first stage suction cooler, first stage suction scrubber, first stage
> compressor and first stage discharge coolers. The data is continuously available and free of charge.
>
>By sharing this live stream of industrial data freely, Aker BP and Cognite hope to accelerate innovation within data-heavy fields. This includes predictive maintenance, condition
> monitoring, and advanced visualization techniques, as well as other new, unexpected applications. Advancement in these areas will directly benefit Aker BP’s operations and will also
>improve the health and outlook of the industrial ecosystem on the Norwegian Continental Shelf.

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

The jupyter notebook will show you how to query the data model using the Cognite Python SDK. The time series loaded in the data set are used to explore
various modes of operation for a compressor on Valhall.

See [Valhall Operational States 2.ipynb](./Valhall%20Operational%20States%202.ipynb)

## Use Charts

You can also use the Charts application to explore the data. Search for time series and add them to your chart.
