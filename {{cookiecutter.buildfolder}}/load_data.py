#!/usr/bin/env python
import os
import click
import sys
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from dotenv import load_dotenv
from inventory import examples_config
import pandas as pd


@click.command()
@click.option("--file", default="", help="Specify a specific table to load.")
@click.option("--drop", default=False, help="Whether to delete existing data.")
@click.argument("example_folder")
def cli(file: str, drop: bool, example_folder: str):
    load_raw(file, drop, example_folder)


def load_raw(file, drop, example_folder):
    # This creation of a CogniteClient() uses client credentials and environment variables.
    # This approach can be reused for any usage of the Cognite Python SDK.
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
    try:
        # Using the token/inspect endpoint to check if the client has access to the project.
        # The response also includes access rights, which can be used to check if the client has the
        # correct access for what you want to do.
        resp = client.get("/api/v1/token/inspect").json()
        if resp is None or len(resp) == 0:
            click.echo(f"CDF client does not have access to your project.")
            exit(1)
    except:
        click.echo("Failure when trying to check login status with CDF.")
        exit(1)
    # The name of the raw database to create is picked up from the inventory.py file, which
    # again is templated with cookiecutter based on the user's input.
    raw_db = examples_config.get(example_folder, {}).get("raw_db", "")
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
                click.echo(
                    f"Failed to upload {f} for example {example_folder}: {e.message}"
                )
                exit(1)
        click.echo(f"Successfully uploaded {f} to {raw_db}.")
    click.echo(f"Successfully uploaded {len(files)} files to {raw_db}.")


if __name__ == "__main__":
    gettrace = sys.gettrace()
    debug_status = True if gettrace else False

    if debug_status:
        load_dotenv("../.env")
        examples_config = {
            "movie_actors": {
                "raw_db": "test_movies",
            },
            "apm_simple": {
                "raw_db": "test_apm_simple",
            },
        }
    else:
        load_dotenv()
    cli()
