#!/usr/bin/env python

# Copyright 2023 Cognite AS
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
from cognite.client.data_classes.data_modeling import ViewId
from utils.transformations_config import parse_transformation_configs
from utils import ToolGlobals
import pandas as pd


@click.command()
@click.option(
    "--dry-run",
    default=False,
    is_flag=True,
    help="Do not delete anything for data models, just simulate",
)
@click.option(
    "--delete",
    default="raw,timeseries,files,transformations,datamodel,instances",
    help="Specify which data you want to delete. Default raw,timeseries,files,transformations,datamodel(all), instances.",
)
@click.argument("example_folder")
def cli(delete: str, example_folder: str, dry_run: bool):
    # Configure the ToolGlobals singleton with the example folder
    # It will then pick up the right configuration from the inventory.json file
    ToolGlobals.example = example_folder
    if dry_run:
        click.echo("DRY RUN: no deletions will be done...")
    if "raw" in delete:
        delete_raw(dry_run=dry_run)
    if "files" in delete:
        delete_files(dry_run=dry_run)
    if "timeseries" in delete:
        delete_timeseries(dry_run=dry_run)
    if "transformations" in delete:
        delete_transformations(dry_run=dry_run)
    if "instances" in delete and "datamodel" not in delete:
        delete_datamodel(instances_only=True, dry_run=dry_run)
    if "datamodel" in delete:
        delete_datamodel(instances_only=False, dry_run=dry_run)
    if ToolGlobals.failed and not dry_run:
        click.echo(f"Failure to delete as expected.")
        exit(1)


def delete_raw(dry_run=False) -> None:
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
                if not dry_run:
                    client.raw.tables.delete(raw_db, table.name)
        if not dry_run:
            client.raw.databases.delete(raw_db)
        click.echo(f"Deleted {raw_db} for example {ToolGlobals.example}.")
    except:
        click.echo(
            f"Failed to delete {raw_db} for example {ToolGlobals.example}. It may not exist."
        )
        ToolGlobals.failed = True


def delete_files(dry_run=False) -> None:
    try:
        client = ToolGlobals.verify_client(capabilities={"filesAcl": ["READ", "WRITE"]})
    except Exception as e:
        click.echo(f"Failed to verify client for example {ToolGlobals.example}")
        click.echo(e)
        ToolGlobals.failed = True
        return
    files = []
    # Pick up all the files in the files folder of the example.
    for _, _, filenames in os.walk(f"./examples/{ToolGlobals.example}/data/files"):
        for f in filenames:
            files.append(ToolGlobals.example + "_" + f)
    if len(files) == 0:
        return
    count = 0
    for f in files:
        try:
            if not dry_run:
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


def delete_timeseries(dry_run=False) -> None:
    """Delete timeseries from CDF based on json files in the example"""

    client = ToolGlobals.verify_client(
        capabilities={"timeseriesAcl": ["READ", "WRITE"]}
    )
    files = []
    # Pick up all the .json files in the data folder of the example.
    for _, _, filenames in os.walk(
        f"./examples/{ToolGlobals.example}/data/timeseries/"
    ):
        for f in filenames:
            if ".json" in f:
                files.append(f)
    # Read timeseries metadata to build a list of TimeSeries
    timeseries: list[TimeSeries] = []
    for f in files:
        with open(
            f"./examples/{ToolGlobals.example}/data/timeseries/{f}", "rt"
        ) as file:
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
            if not dry_run:
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


def delete_transformations(dry_run=False) -> None:
    client = ToolGlobals.verify_client(
        capabilities={"transformationsAcl": ["READ", "WRITE"]}
    )
    configs = parse_transformation_configs(
        f"./examples/{ToolGlobals.example}/transformations/"
    )
    transformations_ext_ids = [t.external_id for t in configs.values()]
    try:
        if not dry_run:
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


def delete_datamodel(instances_only=True, dry_run=False) -> None:
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
        view_list = []
    else:
        view_list = [
            (space_name, d.external_id, d.version) for d in data_model.data[0].views
        ]
    click.echo(f"Found {len(view_list)} views in the data model: {model_name}")
    # It's best practice to delete edges first as edges are deleted when nodes are deleted,
    # but this cascading delete is more expensive than deleting the edges directly.
    #
    # Find any edges in the space
    # Iterate over all the edges in the view 1,000 at the time
    edge_count = 0
    edge_delete = 0
    for instance_list in client.data_modeling.instances(
        instance_type="edge",
        include_typing=False,
        filter={"equals": {"property": ["edge", "space"], "value": space_name}},
        chunk_size=1000,
    ):
        instances = [(space_name, i.external_id) for i in instance_list.data]
        if not dry_run:
            ret = client.data_modeling.instances.delete(edges=instances)
            edge_delete += len(ret.edges)
        edge_count += len(instance_list)
    click.echo(
        f"Found {edge_count} edges and deleted {edge_delete} edges from space {space_name}."
    )
    # For all the views in this data model...
    for _, id, version in view_list:
        node_count = 0
        node_delete = 0
        # Iterate over all the nodes in the view 1,000 at the time
        for instance_list in client.data_modeling.instances(
            instance_type="node",
            include_typing=False,
            sources=ViewId(space_name, id, version),
            chunk_size=1000,
        ):
            instances = [(space_name, i.external_id) for i in instance_list.data]
            if not dry_run:
                ret = client.data_modeling.instances.delete(nodes=instances)
                node_delete += len(ret.nodes)
            node_count += len(instance_list)
        click.echo(
            f"Found {node_count} nodes and deleted {node_delete} nodes from {id} in {model_name}."
        )
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
    click.echo(
        f"Found {len(container_list)} containers in the space {space_name} for example {ToolGlobals.example}"
    )
    # Find any remaining nodes in the space
    node_count = 0
    node_delete = 0
    for instance_list in client.data_modeling.instances(
        instance_type="node",
        include_typing=False,
        filter={"equals": {"property": ["node", "space"], "value": space_name}},
        chunk_size=1000,
    ):
        instances = [(space_name, i.external_id) for i in instance_list.data]
        if not dry_run:
            ret = client.data_modeling.instances.delete(instances)
            node_delete += len(ret.nodes)
        node_count += len(instance_list)
    click.echo(
        f"Found {node_count} nodes and deleted {node_delete} auto-generated nodes (not belonging to a view) from {space_name}."
    )
    if instances_only:
        return
    try:
        if len(container_list) > 0:
            if not dry_run:
                client.data_modeling.containers.delete(container_list)
            click.echo(
                f"Deleted {len(container_list)} containers in data model {model_name}."
            )
    except Exception as e:
        click.echo(
            f"Failed to delete containers in {space_name} for example {ToolGlobals.example}"
        )
        click.echo(e)
        ToolGlobals.failed = True
    try:
        if len(view_list) > 0:
            if not dry_run:
                client.data_modeling.views.delete(view_list)
            click.echo(f"Deleted {len(view_list)} views in data model {model_name}.")
    except Exception as e:
        click.echo(
            f"Failed to delete views in {space_name} for example {ToolGlobals.example}"
        )
        click.echo(e)
        ToolGlobals.failed = True
    try:
        if len(container_list) > 0 or len(view_list) > 0:
            if not dry_run:
                client.data_modeling.data_models.delete((space_name, model_name, "1"))
            click.echo(f"Deleted the data model {model_name}.")
    except Exception as e:
        click.echo(
            f"Failed to delete data model in {space_name} for example {ToolGlobals.example}"
        )
        click.echo(e)
        ToolGlobals.failed = True
    try:
        space = client.data_modeling.spaces.retrieve(space_name)
        if space is not None:
            if not dry_run:
                client.data_modeling.spaces.delete(space_name)
            click.echo(f"Deleted the space {space_name}.")
    except Exception as e:
        click.echo(
            f"Failed to delete space {space_name} for example {ToolGlobals.example}"
        )
        click.echo(e)
        ToolGlobals.failed = True


if __name__ == "__main__":
    cli()
