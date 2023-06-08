#!/usr/bin/env python

# Copyright 2023 Gognite AS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import click
import json
from cognite.client.data_classes.time_series import TimeSeries
from utils import ToolGlobals
import pandas as pd


@click.command()
@click.option("--file", default="", help="Specify a specific table to load.")
@click.option(
    "--load",
    default="raw,timeseries,files",
    help="Specify which data you want to load, default raw,timeseries,files.",
)
@click.option("--drop", default=False, help="Whether to delete existing data.")
@click.argument("example_folder")
def cli(file: str, load: str, drop: bool, example_folder: str):
    # Configure the ToolGlobals singleton with the example folder
    # It will then pick up the right configuration from the inventory.json file
    ToolGlobals.example = example_folder
    if "raw" in load:
        load_raw(file, drop)
    if "files" in load:
        load_files(file, drop)
    if "timeseries" in load:
        load_timeseries(file, drop)
    if ToolGlobals.failed:
        click.echo(f"Failure to load as expected.")
        exit(1)


def load_raw(file: str, drop: bool) -> None:
    """Load raw data from csv files into CDF Raw

    Args:
        file: name of file to load, if empty load all files
        drop: whether to drop existing data
    """
    client = ToolGlobals.verify_client(capabilities={"rawAcl": ["READ", "WRITE"]})
    # The name of the raw database to create is picked up from the inventory.py file, which
    # again is templated with cookiecutter based on the user's input.
    raw_db = ToolGlobals.config("raw_db")
    if raw_db == "":
        click.echo(
            f"Could not find raw_db in inventory.py for example {ToolGlobals.example}."
        )
        ToolGlobals.failed = True
        return
    try:
        if drop:
            tables = client.raw.tables.list(raw_db)
            if len(tables) > 0:
                for table in tables:
                    client.raw.tables.delete(raw_db, table.name)
            client.raw.databases.delete(raw_db)
            click.echo(f"Deleted {raw_db} for example {ToolGlobals.example}.")
    except:
        click.echo(
            f"Failed to delete {raw_db} for example {ToolGlobals.example}. It may not exist."
        )
    try:
        # Creating the raw database and tables is actually not necessary as
        # the SDK will create them automatically when inserting data with insert_dataframe()
        # using the ensure_parent=True argument.
        # However, it is included to show how you can use the SDK.
        client.raw.databases.create(raw_db)
    except Exception as e:
        click.echo(
            f"Failed to create {raw_db} for example {ToolGlobals.example}: {e.message}"
        )
        ToolGlobals.failed = True
        return
    files = []
    if file:
        # Only load the supplied filename.
        files.append(file)
    else:
        # Pick up all the .csv files in the data folder of the example.
        for _, _, filenames in os.walk(f"./{ToolGlobals.example}/data/raw"):
            for f in filenames:
                if ".csv" in f:
                    files.append(f)
    if len(files) == 0:
        return
    click.echo(f"Uploading {len(files)} .csv files to {raw_db} RAW database...")
    for f in files:
        with open(f"./{ToolGlobals.example}/data/raw/{f}", "rt") as file:
            dataframe = pd.read_csv(file, dtype=str)
            dataframe = dataframe.fillna("")
            try:
                client.raw.rows.insert_dataframe(
                    db_name=raw_db,
                    table_name=f[:-4],
                    dataframe=dataframe,
                    ensure_parent=True,
                )
            except Exception as e:
                click.echo(f"Failed to upload {f} for example {ToolGlobals.example}")
                click.echo(e)
                ToolGlobals.failed = True
                return
    click.echo(
        f"Successfully uploaded {len(files)} raw csv files to {raw_db} RAW database."
    )


def load_files(file: str, drop: bool) -> None:
    try:
        client = ToolGlobals.verify_client(capabilities={"filesAcl": ["READ", "WRITE"]})
        files = []
        if file is not None and len(file) > 0:
            files.append(file)
        else:
            # Pick up all the files in the files folder of the example.
            for _, _, filenames in os.walk(f"./{ToolGlobals.example}/data/files"):
                for f in filenames:
                    files.append(f)
        if len(files) == 0:
            return
        click.echo(f"Uploading {len(files)} files/documents to CDF...")
        for f in files:
            client.files.upload(
                path=f"./{ToolGlobals.example}/data/files/{f}",
                data_set_id=ToolGlobals.data_set_id,
                name=f,
                external_id=ToolGlobals.example + "_" + f,
                overwrite=drop,
            )
        click.echo(
            f"Uploaded successfully {len(files)} files/documents from ./{ToolGlobals.example}/data/files"
        )
    except Exception as e:
        click.echo(f"Failed to upload files for example {ToolGlobals.example}")
        click.echo(e)
        ToolGlobals.failed = True
        return


def load_timeseries(file: str, drop: bool) -> None:
    load_timeseries_metadata(file, drop)
    load_timeseries_datapoints(file)


def load_timeseries_metadata(file: str, drop: bool) -> None:
    client = ToolGlobals.verify_client(
        capabilities={"timeseriesAcl": ["READ", "WRITE"]}
    )
    files = []
    if file:
        # Only load the supplied filename.
        files.append(file)
    else:
        # Pick up all the .json files in the data folder of the example.
        for _, _, filenames in os.walk(f"./{ToolGlobals.example}/data/timeseries/"):
            for f in filenames:
                if ".json" in f:
                    files.append(f)
    # Read timeseries metadata
    timeseries: list[TimeSeries] = []
    for f in files:
        with open(f"./{ToolGlobals.example}/data/timeseries/{f}", "rt") as file:
            ts = json.load(file)
            for t in ts:
                timeseries.append(TimeSeries._load(t))
    if len(timeseries) == 0:
        return
    drop_ts: list[str] = []
    for t in timeseries:
        # Set the context info for this CDF project
        t.data_set_id = ToolGlobals.data_set_id
        if drop:
            drop_ts.append(t.external_id)
    try:
        if drop:
            client.time_series.delete(external_id=drop_ts, ignore_unknown_ids=True)
            click.echo(
                f"Deleted {len(drop_ts)} timeseries for example {ToolGlobals.example}."
            )
    except Exception as e:
        click.echo(
            f"Failed to delete {t.external_id} for example {ToolGlobals.example}. It may not exist."
        )
    try:
        client.time_series.create(timeseries)
    except Exception as e:
        click.echo(f"Failed to upload timeseries for example {ToolGlobals.example}.")
        click.echo(e)
        ToolGlobals.failed = True
        return
    click.echo(f"Loaded {len(timeseries)} timeseries from {len(files)} files.")


def load_timeseries_datapoints(file: str) -> None:
    client = ToolGlobals.verify_client(
        capabilities={"timeseriesAcl": ["READ", "WRITE"]}
    )
    files = []
    if file:
        # Only load the supplied filename.
        files.append(file)
    else:
        # Pick up all the .csv files in the data folder of the example.
        for _, _, filenames in os.walk(
            f"./{ToolGlobals.example}/data/timeseries/datapoints/"
        ):
            for f in filenames:
                if ".csv" in f:
                    files.append(f)
    if len(files) == 0:
        return
    click.echo(
        f"Uploading {len(files)} .csv file(s) as datapoints to CDF timeseries..."
    )
    try:
        for f in files:
            with open(
                f"./{ToolGlobals.example}/data/timeseries/datapoints/{f}", "rt"
            ) as file:
                dataframe = pd.read_csv(file, parse_dates=True, index_col=0)
            click.echo(f"Uploading {f} as datapoints to CDF timeseries...")
            client.time_series.data.insert_dataframe(dataframe)
        click.echo(
            f"Uploaded {len(files)} .csv file(s) as datapoints to CDF timeseries."
        )
    except Exception as e:
        click.echo(f"Failed to upload datapoints for example {ToolGlobals.example}.")
        click.echo(e)
        ToolGlobals.failed = True
        return


if __name__ == "__main__":
    cli()
