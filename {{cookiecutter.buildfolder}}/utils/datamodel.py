import datetime
import json
from cognite.client.data_classes.data_modeling import (
    ViewId,
    DirectRelationReference,
    DirectRelation,
)
from cognite.client.data_classes.data_modeling.data_models import DataModel
from cognite.client.data_classes.data_modeling.views import View
from cognite.client.data_classes.data_modeling.spaces import SpaceApply
from cognite.client.data_classes.data_modeling.containers import Container
from .delete import delete_datamodel

from .utils import CDFToolConfig


def load_datamodel(ToolGlobals: CDFToolConfig, drop: bool) -> None:
    with open(f"./examples/{ToolGlobals.example}/datamodel.graphql", "rt") as file:
        # Read directly into a string.
        datamodel = file.read()
    if drop:
        delete_datamodel(ToolGlobals, instances_only=False)
    # Clear any delete errors
    ToolGlobals.failed = False
    client = ToolGlobals.verify_client(
        capabilities={
            "dataModelsAcl": ["READ", "WRITE"],
            "dataModelInstancesAcl": ["READ", "WRITE"],
        }
    )
    space_name = ToolGlobals.config("model_space")
    model_name = ToolGlobals.config("data_model")
    try:
        client.data_modeling.spaces.apply(
            SpaceApply(
                space=space_name,
                name=space_name,
                description=f"Space for {ToolGlobals.example} example",
            )
        )
    except Exception as e:
        print(f"Failed to write space {space_name} for example {ToolGlobals.example}.")
        print(e)
        ToolGlobals.failed = True
        return
    print(f"Created space {space_name}.")
    try:
        client.data_modeling.graphql.apply_dml(
            (space_name, model_name, "1"),
            dml=datamodel,
            name=model_name,
            description=f"Data model for {ToolGlobals.example} example",
        )
    except Exception as e:
        print(
            f"Failed to write data model {model_name} to space {space_name} for example {ToolGlobals.example}."
        )
        print(e)
        ToolGlobals.failed = True
        return
    print(f"Created data model {model_name}.")


def load_datamodel_dump(ToolGlobals: CDFToolConfig, drop: bool) -> None:
    with open(
        f"./examples/{ToolGlobals.example}/data_model/datamodel.json", "rt"
    ) as file:
        # Read directly into DataModel and convert to apply (write) version of datamodel.
        # The json is a direct dump from API /models/datamodels/byids.
        datamodel = DataModel.load(json.load(file)).as_apply()
    views = {}
    containers = {}
    for v in datamodel.views:
        with open(
            f"./examples/{ToolGlobals.example}/data_model/{v.external_id}.view.json",
            "rt",
        ) as file:
            # Load view and convert to apply (write) version of view as we are reading
            # in a dump from a file.
            # The dump is from API /models/views/byids.
            views[v.external_id] = View.load(json.load(file)).as_apply()
        with open(
            f"./examples/{ToolGlobals.example}/data_model/{v.external_id}.container.json",
            "rt",
        ) as file:
            # Load container and convert to apply (write) version of view as we are reading
            # in a dump from a file.
            # The dump is from API /models/containers
            containers[v.external_id] = Container.load(json.load(file)).as_apply()

    if drop:
        delete_datamodel(ToolGlobals, instances_only=False)
    # Clear any delete errors
    ToolGlobals.failed = False
    client = ToolGlobals.verify_client(
        capabilities={
            "dataModelsAcl": ["READ", "WRITE"],
            "dataModelInstancesAcl": ["READ", "WRITE"],
        }
    )
    space_name = ToolGlobals.config("model_space")
    model_name = ToolGlobals.config("data_model")
    try:
        client.data_modeling.spaces.apply(
            SpaceApply(
                space=space_name,
                name=space_name,
                description=f"Space for {ToolGlobals.example} example",
            )
        )
    except Exception as e:
        print(f"Failed to write space {space_name} for example {ToolGlobals.example}.")
        print(e)
        ToolGlobals.failed = True
        return
    print(f"Created space {space_name}.")
    try:
        client.data_modeling.containers.apply([c for c in containers.values()])
        print(f"Created {len(containers)} containers.")
    except Exception as e:
        print(f"Failed to write containers for example {ToolGlobals.example}.")
        print(e)
        ToolGlobals.failed = True
        return
    try:
        client.data_modeling.views.apply([v for v in views.values()])
        print(f"Created {len(views)} views.")
    except Exception as e:
        print(f"Failed to write views for example {ToolGlobals.example}.")
        print(e)
        ToolGlobals.failed = True
        return
    try:
        client.data_modeling.data_models.apply(datamodel)
    except Exception as e:
        print(
            f"Failed to write data model {model_name} for example {ToolGlobals.example}."
        )
        print(e)
        ToolGlobals.failed = True
        return
    print(f"Created data model {model_name}.")


def describe_datamodel(ToolGlobals: CDFToolConfig, space_name, model_name) -> None:
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
                if d.source is None:
                    print(f"{p} has no source")
                    continue
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


def dump_datamodel(
    ToolGlobals: CDFToolConfig, space_name, model_name, target_dir
) -> None:
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
