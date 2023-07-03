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

import sys
import os
import json
import datetime
from cognite.client.data_classes.data_modeling import (
    ViewId,
    DirectRelationReference,
    DirectRelation,
)
from utils import ToolGlobals
import pandas as pd


def describe_datamodel(space_name, model_name, target_dir) -> None:
    """Describe data model from CDF"""

    print("Verifying access rights...")
    client = ToolGlobals.verify_client(
        capabilities={
            "dataModelsAcl": ["READ", "WRITE"],
            "dataModelInstancesAcl": ["READ", "WRITE"],
        }
    )
    print("Loading data model ({model_name}) in space ({space_name})...")
    try:
        print("  space...")
        space = client.data_modeling.spaces.retrieve(space_name)
    except Exception as e:
        print(f"Failed to retrieve space {space_name}.")
        print(e)
    try:
        print("  containers...")
        containers = client.data_modeling.containers.list(space=space_name, limit=None)
    except Exception as e:
        print(f"Failed to retrieve containers for data model {model_name}.")
        print(e)
        return
    containers = containers.data
    try:
        print("  data model...")
        data_model = client.data_modeling.data_models.retrieve(
            (space_name, model_name, "1"), inline_views=False
        )
        data_model = data_model.data[0].dump()
    except Exception as e:
        print(f"Failed to retrieve data model {model_name} in space {space_name}.")
        print(e)
        return
    if len(data_model) == 0:
        print(f"Failed to retrieve data model {model_name} in space {space_name}.")
        return
    try:
        print("  views...")
        views = client.data_modeling.data_models.retrieve(
            (space_name, model_name, "1"), inline_views=True
        )
    except Exception as e:
        print(
            f"Failed to retrieve data model with views {model_name} in space {space_name}."
        )
        print(e)
        return
    views = views.data[0].views
    print("Writing...")
    with open(
        f"{target_dir}/datamodel.json",
        "wt",
    ) as file:
        json.dump(data_model, file, indent=4)
    for v in views:
        with open(
            f"{target_dir}/{v.external_id}.view.json",
            "wt",
        ) as file:
            json.dump(v.dump(), file, indent=4)
    for c in containers:
        with open(
            f"{target_dir}/{c.external_id}.container.json",
            "wt",
        ) as file:
            json.dump(c.dump(), file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: ./dump_datamodel.py <space> <data_model> <directory>")
        exit(1)
    if not os.path.exists(sys.argv[3]):
        os.makedirs(sys.argv[3])
    describe_datamodel(
        space_name=sys.argv[1], model_name=sys.argv[2], target_dir=sys.argv[3]
    )
