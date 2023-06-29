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
import datetime
from cognite.client.data_classes.data_modeling import (
    ViewId,
    Edge,
    Node,
    DirectRelationReference,
    DirectRelation,
)
from utils import ToolGlobals
import pandas as pd


def describe_datamodel(space_name, model_name) -> None:
    """Describe data model from CDF"""

    print("Describing data model ({model_name}) in space ({space_name})...")
    print("Verifying access rights...")
    client = ToolGlobals.verify_client(
        capabilities={
            "dataModelsAcl": ["READ", "WRITE"],
            "dataModelInstancesAcl": ["READ", "WRITE"],
        }
    )
    try:
        space = client.data_modeling.spaces.retrieve(space_name)
        print(
            f"Found the space {space_name} with name ({space.name}) and description ({space.description})."
        )
        print(
            f"  - created_time: {datetime.datetime.fromtimestamp(space.created_time/1000)}"
        )
        print(
            f"  - last_updated_time: {datetime.datetime.fromtimestamp(space.last_updated_time/1000)}"
        )
    except Exception as e:
        print(f"Failed to retrieve space {space_name}.")
        print(e)
    try:
        containers = client.data_modeling.containers.list(space=space_name, limit=None)
    except Exception as e:
        print(f"Failed to retrieve containers for data model {model_name}.")
        print(e)
        return
    container_list = [(space_name, c.external_id) for c in containers.data]
    print(f"Found {len(container_list)} containers in the space {space_name}:")
    for c in container_list:
        print(f"  {c[1]}")
    try:
        data_model = client.data_modeling.data_models.retrieve(
            (space_name, model_name, "1"), inline_views=True
        )
    except Exception as e:
        print(f"Failed to retrieve data model {model_name} in space {space_name}.")
        print(e)
        return
    if len(data_model) == 0:
        print(f"Failed to retrieve data model {model_name} in space {space_name}.")
        return
    print(f"Found data model {model_name} in space {space_name}:")
    print(f"  version: {data_model.data[0].version}")
    print(f"  global: {'True' if data_model.data[0].is_global else 'False'}")
    print(f"  description: {data_model.data[0].description}")
    print(
        f"  created_time: {datetime.datetime.fromtimestamp(data_model.data[0].created_time/1000)}"
    )
    print(
        f"  last_updated_time: {datetime.datetime.fromtimestamp(data_model.data[0].last_updated_time/1000)}"
    )
    views = data_model.data[0].views
    print(f"  {model_name} has {len(views)} views:")
    direct_relations = 0
    edge_relations = 0
    for v in views:
        print(f"    {v.external_id}, version: {v.version}")
        print(f"       - properties: {len(v.properties)}")
        print(f"       - used for {v.used_for}s")
        print(f"       - implements: {v.implements}")
        for p, d in v.properties.items():
            if type(d.type) is DirectRelation:
                direct_relations += 1
                print(
                    f"       - direct relation 1:1 {p} --> ({d.source.space}, {d.source.external_id}, {d.source.version})"
                )
            elif type(d.type) is DirectRelationReference:
                edge_relations += 1
                print(
                    f"       - edge relation 1:MANY {p} -- {d.direction} --> ({d.source.space}, {d.source.external_id}, {d.source.version})"
                )

    print(f"Total direct relations: {direct_relations}")
    print(f"Total edge relations: {edge_relations}")
    print(f"------------------------------------------")

    # Find any edges in the space
    # Iterate over all the edges in the view 1,000 at the time
    edge_count = 0
    edge_relations = {}
    for instance_list in client.data_modeling.instances(
        instance_type="edge",
        include_typing=False,
        filter={"equals": {"property": ["edge", "space"], "value": space_name}},
        chunk_size=1000,
    ):
        for i in instance_list.data:
            if type(i.type) is DirectRelationReference:
                if edge_relations.get(i.type.external_id) is None:
                    edge_relations[i.type.external_id] = 0
                edge_relations[i.type.external_id] += 1
        edge_count += len(instance_list.data)
    sum = 0
    for count in edge_relations.values():
        sum += count
    print(
        f"Found in total {edge_count} edges in space {space_name} spread over {len(edge_relations)} types:"
    )
    for d, c in edge_relations.items():
        print(f"  {d}: {c}")
    print("------------------------------------------")
    # Find all nodes in the space
    node_count = 0
    for instance_list in client.data_modeling.instances(
        instance_type="node",
        include_typing=False,
        filter={"equals": {"property": ["node", "space"], "value": space_name}},
        chunk_size=1000,
    ):
        node_count += len(instance_list)
    print(
        f"Found in total {node_count} nodes in space {space_name} across all views and containers."
    )
    # For all the views in this data model...
    for v in views:
        node_count = 0
        # Iterate over all the nodes in the view 1,000 at the time
        for instance_list in client.data_modeling.instances(
            instance_type="node",
            include_typing=False,
            sources=ViewId(space_name, v.external_id, v.version),
            chunk_size=1000,
        ):
            node_count += len(instance_list)
        print(f"  {node_count} nodes of view {v.external_id}.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./describe_datamodel.py <space> <data_model>")
        exit(1)
    describe_datamodel(space_name=sys.argv[1], model_name=sys.argv[2])
