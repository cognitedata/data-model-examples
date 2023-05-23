#!/usr/bin/env python
import os
import click
import sys
from cognite.client import CogniteClient, ClientConfig
from cognite.client.exceptions import CogniteAuthError, CogniteException
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes.data_sets import DataSet
from dotenv import load_dotenv
from inventory import ExamplesConfig
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
    if "raw" in load:
        load_raw(file, drop, example_folder)
    if "files" in load:
        load_files(file, drop, example_folder)


def verify_dataset(example: str) -> int | None:
    """Verify that the data set exists

    Args:
        example: name of example folder used to look up dataset in ExamplesConfig in inventory.py
    Yields:
        data_set_id (int)
        Re-raises underlying SDK exception
    """

    def get_dataset_name(example) -> str:
        return (
            "tutorial_dataset"
            if examples_config.get(example, "data_set") == ""
            else examples_config.get(example, "data_set")
        )

    client = verify_client(capabilities={"datasetsAcl": ["READ", "WRITE"]})
    try:
        data_set = client.data_sets.retrieve(external_id=get_dataset_name(example))
        if data_set is not None:
            return data_set.id
    except Exception as e:
        raise e
    try:
        data_set = DataSet(
            external_id=get_dataset_name(example),
            description="Test data set for tutorials",
        )
        data_set = client.data_sets.create(data_set)
        return data_set.id
    except Exception as e:
        raise e


def verify_client(capabilities: dict[list] = {}, data_set_id=0) -> CogniteClient:
    """Verify that the client has correct credentials and required access rights

    Supply requirement CDF ACLs to verify if you have correct access
    capabilities = {
        "filesAcl": ["READ", "WRITE"],
        "datasetsAcl": ["READ", "WRITE"]
    }
    This approach can be reused for any usage of the Cognite Python SDK.

    Args:
        capabilities (dict[list], optional): access capabilities to verify
        data_set_id (int): id of dataset that access should be granted to

    Yields:
        CogniteClient: Verified client with access rights
        Re-raises underlying SDK exception
    """
    try:
        # Using the token/inspect endpoint to check if the client has access to the project.
        # The response also includes access rights, which can be used to check if the client has the
        # correct access for what you want to do.
        resp = client.get("/api/v1/token/inspect").json()
        if resp is None or len(resp) == 0:
            raise CogniteAuthError(f"Don't have any access rights. Check credentials.")
    except Exception as e:
        raise e
    # iterate over all the capabilties we need
    for cap, actions in capabilities.items():
        # Find the right capability in our granted capabilities
        for k in resp.get("capabilities", []):
            if len(k.get(cap, {})) == 0:
                continue
            # For each of the actions (e.g. READ or WRITE) we need, check if we have it
            for a in actions:
                if a not in k.get(cap, {}).get("actions", []):
                    raise CogniteAuthError(
                        f"Don't have correct access rights. Need {a} on {cap}"
                    )
            # Check if we either have all scope or data_set_id scope
            if "all" not in k.get(cap, {}).get("scope", {}) and (
                data_set_id != 0
                and str(data_set_id)
                not in k.get(cap, {})
                .get("scope", {})
                .get("datasetScope")
                .get("ids", [])
            ):
                raise CogniteAuthError(
                    f"Don't have correct access rights. Need {a} on {cap}"
                )
            continue
    return client


def load_raw(file: str, drop: bool, example_folder: str) -> None:
    client = verify_client(capabilities={"rawAcl": ["READ", "WRITE"]})
    # The name of the raw database to create is picked up from the inventory.py file, which
    # again is templated with cookiecutter based on the user's input.
    raw_db = examples_config.get(example_folder, "raw_db")
    if raw_db == "":
        click.echo(
            f"Could not find raw_db in inventory.py for example {example_folder}."
        )
        exit(1)
    try:
        if drop:
            tables = client.raw.tables.list(raw_db)
            if len(tables) > 0:
                for table in tables:
                    client.raw.tables.delete(raw_db, table.name)
            client.raw.databases.delete(raw_db)
    except:
        click.echo(
            f"Failed to delete {raw_db} for example {example_folder}. It may not exist."
        )
    try:
        # Creating the raw database and tables is actually not necessary as
        # the SDK will create them automatically when inserting data with insert_dataframe()
        # using the ensure_parent=True argument.
        # However, it is included to show how you can use the SDK.
        client.raw.databases.create(raw_db)
    except Exception as e:
        click.echo(
            f"Failed to create {raw_db} for example {example_folder}: {e.message}"
        )
        exit(1)
    files = []
    if file:
        # Only load the supplied filename.
        files.append(file)
    else:
        # Pick up all the .csv files in the data folder of the example.
        for _, _, filenames in os.walk(f"./{example_folder}/data/raw"):
            for f in filenames:
                if ".csv" in f:
                    files.append(f)
    for f in files:
        with open(f"./{example_folder}/data/raw/{f}", "rt") as file:
            click.echo(f"Uploading {f} to {raw_db}...")
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
                click.echo(f"Failed to upload {f} for example {example_folder}")
                click.echo(e)
                exit(1)
        click.echo(f"Successfully uploaded {f} to {raw_db}.")
    click.echo(f"Successfully uploaded {len(files)} raw csv files to {raw_db}.")


def load_files(file: str, drop: bool, example_folder: str) -> None:
    try:
        data_set_id = verify_dataset(example_folder)
        client = verify_client(
            capabilities={"filesAcl": ["READ", "WRITE"]}, data_set_id=data_set_id
        )
        files = []
        if file is not None and len(file) > 0:
            files.append(file)
        else:
            # Pick up all the files in the files folder of the example.
            for _, _, filenames in os.walk(f"./{example_folder}/data/files"):
                for f in filenames:
                    files.append(f)

        for f in files:
            client.files.upload(
                path=f"./{example_folder}/data/files/{f}",
                data_set_id=data_set_id,
                external_id=example_folder + "_" + f,
                overwrite=drop,
            )
        click.echo(
            f"Uploaded successfully {len(files)} files/documents from ./{example_folder}/data/files"
        )
    except Exception as e:
        click.echo(f"Failed to upload files for example {example_folder}")
        click.echo(e)
        exit(1)


if __name__ == "__main__":
    client = CogniteClient(
        ClientConfig(
            client_name="Cognite examples library 0.1.0",
            base_url=os.environ["CDF_URL"],
            project=os.environ["CDF_PROJECT"],
            credentials=OAuthClientCredentials(
                token_url=os.environ["CDF_TOKEN_URL"],
                client_id=os.environ["CDF_CLIENT_ID"],
                # client secret should not be stored in-code, so we load it from an environment variable
                client_secret=os.environ["CDF_CLIENT_SECRET"],
                scopes=[os.environ["CDF_SCOPES"]],
            ),
        )
    )
    gettrace = sys.gettrace()
    debug_status = True if gettrace else False

    if debug_status:
        load_dotenv("../.env")
        examples_config = ExamplesConfig(
            {
                "movie_actors": {
                    "raw_db": "test_movies",
                    "data_set": "tutorial_movies_dataset",
                },
                "apm_simple": {
                    "raw_db": "test_apm_simple",
                    "data_set": "tutorial_apm_simple_dataset",
                },
            }
        )
    else:
        load_dotenv()
        examples_config = ExamplesConfig()
    cli()
