import csv
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes.raw import Row
import os
from os import walk
import click
from dotenv import load_dotenv
from inventory import examples_config
import sys

gettrace = sys.gettrace()
debug_status = True if gettrace else False

if debug_status:
    load_dotenv("../.env")
    examples_config = {
        "movie_actors": {
            "raw_db": "oid",
            "raw_db_key": "id",
        }
    }
else:
    load_dotenv()


@click.command()
@click.option("--file", default="", help="Specify a specific table to load.")
@click.option("--drop", default=False, help="Whether to delete existing data.")
@click.argument("example_folder")
def load(file, drop, example_folder):
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
        resp = client.get("/api/v1/token/inspect").json()
        if resp is None or len(resp) == 0:
            print(f"CDF client does not have access to your project.")
            exit(1)
    except:
        print("Failure when trying to check login status with CDF.")
        exit(1)
    raw_db = examples_config.get(example_folder, {}).get("raw_db", "")
    if raw_db == "":
        print(f"Could not find raw_db in inventory.py for example {example_folder}.")
        exit(1)
    try:
        if drop:
            tables = client.raw.tables.list(raw_db)
            if len(tables) > 0:
                for table in tables:
                    client.raw.tables.delete(raw_db, table.name)
            client.raw.databases.delete(raw_db)
    except:
        print(f"Failed to delete {raw_db} for example {example_folder}.")
        exit(1)
    try:
        client.raw.databases.create(raw_db)
    except Exception as e:
        print(f"Failed to create {raw_db} for example {example_folder}: {e.message}")
        exit(1)
    files = []
    if file:
        files.append(file)
    else:
        for _, _, filenames in walk(f"./{example_folder}/data/"):
            for f in filenames:
                if ".csv" in f:
                    files.append(f)
    for f in files:
        with open(f"./{example_folder}/data/{f}", "r") as file:
            total = sum(1 for _ in file)
            file.seek(0)
            csv_reader = csv.DictReader(file, delimiter=",")
            count = 0
            rows = []
            key = examples_config.get(example_folder, {}).get("raw_db_key", "")
            if key == "":
                raise BaseException(
                    "Could not find raw_db_key in inventory.py for example {example_folder}."
                )
            print(
                f"Writing {total} rows to RAW database {raw_db} and table {f[:-4]}..."
            )
            for r in csv_reader:
                rows.append(Row(key=key, columns=r.copy()))
                count += 1
                total -= 1
                if count == 1000 or total == 0:
                    try:
                        client.raw.rows.insert(
                            db_name=raw_db,
                            table_name=f[:-4],
                            row=rows,
                            ensure_parent=True,
                        )
                    except Exception as e:
                        print(
                            f"Failed to upload {f} for example {example_folder}: {e.message}"
                        )
                        exit(1)
                    rows = []
                    count = 0


if __name__ == "__main__":
    load()
