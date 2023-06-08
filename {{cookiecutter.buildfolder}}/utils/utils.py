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

import json
import os
import logging
from cognite.client.exceptions import CogniteAuthError
from cognite.client.data_classes.data_sets import DataSet
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials

logger = logging.getLogger(__name__)


# To add a new example, add a new entry here with the same name as the folder
# These values are used by the python scripts.
class CDFToolConfig:
    """Configurations for how to store data in CDF

    Properties:
        client: active CogniteClient
        example: name of the example folder you want to use
    Functions:
        config: configuration for the example (.get("config_name"))
        verify_client: verify that the client has correct credentials and specified access capabilties
        veryify_dataset: verify that the data set exists and that the client has access to it

    To add a new example, add a new entry here with the same name as the folder.
    These values are used by the python scripts.
    """

    def __init__(self, config: dict | None = None) -> None:
        self._data_set_id: int = 0
        self._example = None
        self._failed = False
        if config is not None:
            self._config = config
        else:
            try:
                with open(f"./inventory.json", "rt") as file:
                    self._config = json.load(file)
            except Exception as e:
                logger.error(
                    "Not able to load example inventory from inventory.json file."
                )
                logger.error(e)
                exit(1)

        self._client = CogniteClient(
            ClientConfig(
                client_name="Cognite examples library 0.1.0",
                base_url=os.environ["CDF_URL"],
                project=os.environ["CDF_PROJECT"],
                credentials=OAuthClientCredentials(
                    token_url=os.environ["IDP_TOKEN_URL"],
                    client_id=os.environ["IDP_CLIENT_ID"],
                    # client secret should not be stored in-code, so we load it from an environment variable
                    client_secret=os.environ["IDP_CLIENT_SECRET"],
                    scopes=[os.environ["IDP_SCOPES"]],
                ),
            )
        )

    @property
    # Flag set if something that should have worked failed if a data set is
    # loaded and/or deleted.
    def failed(self) -> bool:
        return self._failed

    @failed.setter
    def failed(self, value: bool):
        self._failed = value

    @property
    def client(self) -> CogniteClient:
        return self._client

    @property
    def data_set_id(self) -> int:
        return self._data_set_id

    # Use this to ignore the data set when verifying the client's access capabilities
    # Set the example property to configure the data set and verify it
    def clear_dataset(self):
        self._data_set_id = 0

    def config(self, attr: str) -> str:
        if attr not in self._config.get(self._example, {}):
            raise ValueError(f"{attr} property must be set in CDFToolConfig().")
        return self._config.get(self._example, {}).get(attr, "")

    @property
    def example(self) -> str:
        return self._example

    @example.setter
    def example(self, value: str):
        if value is None or value not in self._config:
            raise ValueError(
                "example must be set to one of the values in the _config inventory in CDFToolConfig()."
            )
        self._example = value
        # Since we now have a new configuration, check the dataset and set the id
        self._data_set_id = self.verify_dataset()

    def verify_client(self, capabilities: dict[list] = {}) -> CogniteClient:
        """Verify that the client has correct credentials and required access rights

        Supply requirement CDF ACLs to verify if you have correct access
        capabilities = {
            "filesAcl": ["READ", "WRITE"],
            "datasetsAcl": ["READ", "WRITE"]
        }
        The data_set_id will be used when verifying that the client has access to the dataset.
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
            resp = self.client.get("/api/v1/token/inspect").json()
            if resp is None or len(resp) == 0:
                raise CogniteAuthError(
                    f"Don't have any access rights. Check credentials."
                )
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
                    self._data_set_id != 0
                    and str(self._data_set_id)
                    not in k.get(cap, {})
                    .get("scope", {})
                    .get("datasetScope")
                    .get("ids", [])
                ):
                    raise CogniteAuthError(
                        f"Don't have correct access rights. Need {a} on {cap}"
                    )
                continue
        return self._client

    def verify_dataset(self, data_set_name: str = None) -> int | None:
        """Verify that the configured data set exists and is accessible

        This function can be used independent of example config by supplying the data set name.
        It will then ignore the example config and use the supplied name.
        Calling this function directly will not influence verify_client().

        Args:
            data_set_name (str, optional): name of the data set to verify
        Yields:
            data_set_id (int)
            Re-raises underlying SDK exception
        """

        def get_dataset_name() -> str:
            """Helper function to get the dataset name from the inventory.py file"""
            return (
                data_set_name
                if data_set_name is not None and len(data_set_name) > 0
                else self.config("data_set")
            )

        client = self.verify_client(capabilities={"datasetsAcl": ["READ", "WRITE"]})
        try:
            data_set = client.data_sets.retrieve(external_id=get_dataset_name())
            if data_set is not None:
                return data_set.id
        except Exception as e:
            raise e
        try:
            # name can be empty, but is useful for UI purposes
            data_set = DataSet(
                external_id=get_dataset_name(),
                name=get_dataset_name(),
                description=self.config("data_set_desc")
                if self.config("data_set_desc") != ""
                else "Test data set for tutorials",
            )
            data_set = client.data_sets.create(data_set)
            return data_set.id
        except Exception as e:
            raise e
