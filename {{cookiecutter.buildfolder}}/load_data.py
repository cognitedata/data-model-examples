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
@click.option("--file", default="", help="Specify a specific table to load.")
@click.option(
    "--load",
    default="raw,timeseries,files,transformations,datamodel",
    help="Specify which data you want to load. Options: raw,timeseries,files,transformations,transformationsdump,datamodel,datamodeldump.",
)
@click.option(
    "--drop", is_flag=True, default=False, help="Whether to delete existing data."
)
@click.argument("example_folder")
def cli(file: str, load: str, drop: bool, example_folder: str):
    # Configure the ToolGlobals singleton with the example folder
    # It will then pick up the right configuration from the inventory.json file
    ToolGlobals.example = example_folder
    if "raw" in load:
        load_raw(ToolGlobals, file, drop)
    if "files" in load:
        load_files(ToolGlobals, file, drop)
    if "timeseries" in load:
        load_timeseries(ToolGlobals, file, drop)
    if "transformationsdump" in load:
        load_transformations_dump(ToolGlobals, file, drop)
    elif "transformations" in load:
        load_transformations(ToolGlobals, file, drop)
    if "datamodeldump" in load:
        load_datamodel_dump(ToolGlobals, drop)
    elif "datamodel" in load:
        load_datamodel(ToolGlobals, drop)
    if ToolGlobals.failed:
        print(f"Failure to load as expected.")
        exit(1)


if __name__ == "__main__":
    cli()
