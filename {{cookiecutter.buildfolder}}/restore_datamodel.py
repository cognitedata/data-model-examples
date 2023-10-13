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
@click.option("--drop", is_flag=True, default=False, help="Whether to drop data first.")
@click.option("--dry-run", is_flag=True, default=False, help="Whether to do a dry-run.")
@click.argument("folder")
def cli(dry_run: bool, drop: bool, folder: str):
    load_datamodel_dump(ToolGlobals, drop=drop, dry_run=dry_run, directory=folder)
    if ToolGlobals.failed:
        print(f"Failure to load as expected.")
        exit(1)


if __name__ == "__main__":
    cli()
