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
from utils.transformations_config import parse_transformation_configs
from utils import ToolGlobals
import pandas as pd


@click.command()
@click.option(
    "--delete",
    default="raw,timeseries,files,transformations,datamodel,instances",
    help="Specify which data you want to delete. Default raw,timeseries,files,transformations,datamodel(all), instances.",
)
@click.argument("example_folder")
def cli(delete: str, example_folder: str):
    # Configure the ToolGlobals singleton with the example folder
    # It will then pick up the right configuration from the inventory.json file
    ToolGlobals.example = example_folder
    if "raw" in delete:
        delete_raw()
    if "files" in delete:
        delete_files()
    if "timeseries" in delete:
        delete_timeseries()
    if "transformations" in delete:
        delete_transformations()
    if "instances" in delete and "datamodel" not in delete:
        delete_datamodel(instances_only=True)
    if "datamodel" in delete:
        delete_datamodel(instances_only=False)
    if ToolGlobals.failed:
        click.echo(f"Failure to delete as expected.")
        exit(1)


def delete_raw() -> None:
    """Delete raw data from CDF raw based om csv files in the example"""
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
        ToolGlobals.failed = True


def delete_files() -> None:
    try:
        client = ToolGlobals.verify_client(capabilities={"filesAcl": ["READ", "WRITE"]})
    except Exception as e:
        click.echo(f"Failed to verify client for example {ToolGlobals.example}")
        click.echo(e)
        ToolGlobals.failed = True
        return
    files = []
    # Pick up all the files in the files folder of the example.
    for _, _, filenames in os.walk(f"./{ToolGlobals.example}/data/files"):
        for f in filenames:
            files.append(ToolGlobals.example + "_" + f)
    if len(files) == 0:
        return
    count = 0
    for f in files:
        try:
            client.files.delete(external_id=f)
            count += 1
        except Exception as e:
            pass
    if count > 0:
        click.echo(f"Deleted {count} files for example {ToolGlobals.example}")
        return
    click.echo(
        f"Failed to delete files for example {ToolGlobals.example}. They may not exist."
    )
    ToolGlobals.failed = True


def delete_timeseries() -> None:
    """Delete timeseries from CDF based on json files in the example"""

    client = ToolGlobals.verify_client(
        capabilities={"timeseriesAcl": ["READ", "WRITE"]}
    )
    files = []
    # Pick up all the .json files in the data folder of the example.
    for _, _, filenames in os.walk(f"./{ToolGlobals.example}/data/timeseries/"):
        for f in filenames:
            if ".json" in f:
                files.append(f)
    # Read timeseries metadata to build a list of TimeSeries
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
        drop_ts.append(t.external_id)
    count = 0
    for e_id in drop_ts:
        try:
            client.time_series.delete(external_id=e_id, ignore_unknown_ids=False)
            count += 1
        except Exception as e:
            pass
    if count > 0:
        click.echo(f"Deleted {count} timeseries for example {ToolGlobals.example}.")
    else:
        click.echo(
            f"Failed to delete timeseries for example {ToolGlobals.example}. They may not exist."
        )
        ToolGlobals.failed = True


def delete_transformations() -> None:
    client = ToolGlobals.verify_client(
        capabilities={"transformationsAcl": ["READ", "WRITE"]}
    )
    configs = parse_transformation_configs(f"./{ToolGlobals.example}/transformations/")
    transformations_ext_ids = [t.external_id for t in configs.values()]
    try:
        client.transformations.delete(external_id=transformations_ext_ids)
        click.echo(
            f"Deleted {len(transformations_ext_ids)} transformations for example {ToolGlobals.example}."
        )
    except Exception as e:
        click.echo(
            f"Failed to delete transformations for example {ToolGlobals.example}. They may not exist."
        )
        ToolGlobals.failed = True
        return


def delete_datamodel(instances_only=True) -> None:
    """Delete data model from CDF based on the data model in the example

    Note that deleting the data model does not delete the views it consists of or
    the instances stored across one or more containers. Hence, the clean up data, you
    need to retrieve the nodes and edges found in each of the views in the data model,
    delete these, and then delete the containers and views, before finally deleting the
    data model itself.
    """

    client = ToolGlobals.verify_client(
        capabilities={
            "dataModelsAcl": ["READ", "WRITE"],
            "dataModelInstancesAcl": ["READ", "WRITE"],
        }
    )
    space_name = ToolGlobals.config("model_space")
    model_name = ToolGlobals.config("data_model")
    try:
        data_model = client.data_modeling.data_models.retrieve(
            (space_name, model_name, "1")
        )
    except Exception as e:
        click.echo(
            f"Failed to retrieve data model {model_name} for example {ToolGlobals.example}"
        )
        click.echo(e)
        ToolGlobals.failed = True
        return
    if len(data_model) == 0:
        click.echo(
            f"Failed to retrieve data model {model_name} for example {ToolGlobals.example}"
        )
        ToolGlobals.failed = True
        return
    view_list = [
        (space_name, d.external_id, d.version) for d in data_model.data[0].views
    ]
    click.echo(f"Found {len(view_list)} views in the data model: {model_name}")
    views = []
    # For all the views in this data model...
    for _, id, version in view_list:
        # ...retrieve all the instances of the view
        cursors = {}
        instances = []
        while cursors is not None:
            query = {
                "with": {
                    id: {
                        "nodes": {
                            "filter": {
                                "hasData": [
                                    {
                                        "type": "view",
                                        "space": ToolGlobals.config("model_space"),
                                        "externalId": id,
                                        "version": version,
                                    }
                                ]
                            },
                        },
                        "limit": 1000,
                    }
                },
                "select": {id: {}},
            }
            # If we have a cursor, add it to the query
            if len(cursors) > 0:
                query["cursors"] = cursors
            # Retrieve the instances of the view
            try:
                nodes = client.post(
                    "/api/v1/projects/"
                    + client.config.project
                    + "/models/instances/query",
                    json=query,
                ).json()
            except Exception as e:
                click.echo(
                    f"Failed to retrieve instances of view {id} for example {ToolGlobals.example}"
                )
                click.echo(e)
                ToolGlobals.failed = True
                return
            # Build the list of instances needed for deletion
            instances.extend(
                [
                    {
                        "instanceType": i.get("instanceType"),
                        "externalId": i.get("externalId", None),
                        "space": space_name,
                    }
                    for i in nodes.get("items", {}).get(id, [])
                ]
            )
            cursors = nodes.get("nextCursor", {})
            if len(cursors) == 0:
                cursors = None
        start = 0
        count = 0
        while start < len(instances):
            stop = start + 999  # Max number of instances to delete in one request
            if stop > len(instances):
                stop = len(instances)
            try:
                ret = client.post(
                    "/api/v1/projects/"
                    + client.config.project
                    + "/models/instances/delete",
                    json={"items": instances[start:stop]},
                ).json()
            except Exception as e:
                click.echo(
                    f"Failed to delete instances of view {id} for example {ToolGlobals.example}"
                )
                click.echo(e)
                ToolGlobals.failed = True
                return
            count += len(ret.get("items", []))
            start += stop

        print(f"Deleted {count} nodes and edges from {id} in {model_name}.")

    try:
        containers = client.data_modeling.containers.list(
            space=ToolGlobals.config("model_space"), limit=None
        )
    except Exception as e:
        click.echo(f"Failed to retrieve containers for example {ToolGlobals.example}")
        click.echo(e)
        ToolGlobals.failed = True
        return
    container_list = [(space_name, c.external_id) for c in containers.data]
    for _, id in container_list:
        query = {
            "with": {
                id: {
                    "nodes": {
                        "filter": {
                            "hasData": [
                                {
                                    "type": "container",
                                    "space": ToolGlobals.config("model_space"),
                                    "externalId": id,
                                }
                            ]
                        },
                    },
                    "limit": 1000,
                }
            },
            "select": {id: {}},
        }
        try:
            nodes = client.post(
                "/api/v1/projects/" + client.config.project + "/models/instances/query",
                json=query,
            ).json()
        except Exception as e:
            continue
        if len(nodes.get("items", {}).get(id, [])) > 0:
            click.echo(
                f"ERROR! Found {len(nodes)} remaining nodes in the container: {id}"
            )
            ToolGlobals.failed = True
    if instances_only:
        return
    try:
        client.data_modeling.containers.delete(container_list)
        click.echo(
            f"Deleted {len(container_list)} containers in data model {model_name}."
        )
        client.data_modeling.views.delete(view_list)
        click.echo(f"Deleted {len(view_list)} views in data model {model_name}.")
        client.data_modeling.data_models.delete((space_name, model_name, "1"))
        click.echo(f"Deleted the data model {model_name}.")
    except Exception as e:
        click.echo(
            f"Failed to delete containers, views, or data model {model_name} for example {ToolGlobals.example}"
        )
        click.echo(e)
        ToolGlobals.failed = True
        return


if __name__ == "__main__":
    cli()
