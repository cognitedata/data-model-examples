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

import click
from utils import *


@click.command()
@click.option(
    "--dry-run",
    default=False,
    is_flag=True,
    help="Do not delete anything for data models, just simulate",
)
@click.option(
    "--instances",
    default=False,
    is_flag=True,
    help="Also delete instances (nodes and edges)",
)
@click.option(
    "--delete",
    default="raw,timeseries,files,transformations,datamodel,instances",
    help="Specify which data you want to delete. Default raw,timeseries,files,transformations,datamodel,datamodelall,instances",
)
@click.argument("example_folder")
def cli(delete: str, example_folder: str, dry_run: bool, instances: bool):
    if dry_run:
        print("DRY RUN: no deletions will be done...")
    if "datamodelall" in delete:
        if example_folder == "all":
            clean_out_datamodels(ToolGlobals, dry_run=dry_run, instances=instances)
        else:
            print(f"Use 'all' instead of '{example_folder}' to delete everything.")
            print(f"Picking up all containers and views from {example_folder}.")
            clean_out_datamodels(
                ToolGlobals,
                dry_run=dry_run,
                directory=f"./examples/{example_folder}",
                instances=instances,
            )
        exit(0)
    # Configure the ToolGlobals singleton with the example folder
    # It will then pick up the right configuration from the inventory.json file
    ToolGlobals.example = example_folder
    if "raw" in delete:
        delete_raw(ToolGlobals, dry_run=dry_run)
    if "files" in delete:
        delete_files(ToolGlobals, dry_run=dry_run)
    if "timeseries" in delete:
        delete_timeseries(ToolGlobals, dry_run=dry_run)
    if "transformations" in delete:
        delete_transformations(ToolGlobals, dry_run=dry_run)
    if "instances" in delete and "datamodel" not in delete:
        delete_datamodel(ToolGlobals, instances_only=True, dry_run=dry_run)
    if "datamodel" in delete:
        delete_datamodel(ToolGlobals, instances_only=False, dry_run=dry_run)
    if ToolGlobals.failed and not dry_run:
        print(f"Failure to delete as expected.")
        exit(1)


if __name__ == "__main__":
    cli()
