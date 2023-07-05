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
from requests_oauthlib import OAuth2Session
from cognite.client.exceptions import CogniteAuthError
from cognite.client.data_classes.data_sets import DataSet
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials, Token

logger = logging.getLogger(__name__)

import http.server


class AuthPath:
    def __init__(self) -> None:
        self.path = ""


# This is a callback server to get the authorization code from the browser
# It listens on http, but returns https to avoid that the oauth2 library
# complains about the uri not being https.
def getCallback():
    class ServerHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            AuthPath.path = self.path
            self.send_response(200, "Success!")

    HOST = "localhost"
    PORT = 53000
    Handler = ServerHandler
    with http.server.HTTPServer((HOST, PORT), Handler) as httpd:
        print("Web Server listening at => " + HOST + ":" + str(PORT))
        httpd.handle_request()
        return "https://localhost:5300" + AuthPath.path


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

    def __init__(
        self,
        client_name: str = "Generic Cognite examples library",
        config: dict | None = None,
    ) -> None:
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
        # Use lack of IDP_CLIENT_SECRET to determine if we should use the
        # interactive authorization flow.
        if (
            "IDP_CLIENT_SECRET" in os.environ
            and len(os.environ["IDP_CLIENT_SECRET"]) > 0
        ):
            # This is the default configuration for production projects.
            # You then don't have to log in interactively.
            credentials = OAuthClientCredentials(
                token_url=os.environ["IDP_TOKEN_URL"],
                client_id=os.environ["IDP_CLIENT_ID"],
                # client secret should not be stored in-code, so we load it from an environment variable
                client_secret=os.environ["IDP_CLIENT_SECRET"],
                scopes=[os.environ["IDP_SCOPES"]],
                audience=os.environ["IDP_AUDIENCE"],
            )
        else:
            # For trial projects (which are using Authorization Flow), we
            # need to use the interactive authorization flow.
            # NOTE!! The standard Python SDK uses MSAL for OAuth2, a library
            # for ActiveDirectory. The MSAL interactive flow is only supported
            # for ActiveDirectory as an IDP. Hence, we use a separate library
            # for OAuth2, requests_oauthlib, to do the interactive flow.
            # And then we inject the token into the CDF Python SDK using Token()
            # as credentials.
            credentials = OAuth2Session(
                # This client_id is for the Auth0 service principal used for all
                # trial projects. It is not a secret, and can be used by anyone.
                client_id="HkPh5dLe4CF0VOksCYGGrrxjTQ8gCPVL",
                # We need to use these scopes and not the default scope as we are using
                # the Auth0 service principal to authenticate with your user account,
                # and the token will then impersonate the user account.
                scope=["IDENTITY", "user_impersonation"],
                redirect_uri="http://localhost:53000",
            )
            authorization_url, _ = credentials.authorization_url(
                url=os.environ["IDP_AUTHORITY_URL"],
                audience=os.environ["IDP_AUDIENCE"],
            )
            print(
                f"Please click on this link and login to authorize access (THE BROWSER WILL "
                + f"THEN SHOW AN ERROR, just return here): \n{authorization_url}"
            )
            authorization_response = getCallback()
            token = credentials.fetch_token(
                token_url=os.environ["IDP_TOKEN_URL"],
                authorization_response=authorization_response,
                include_client_id=True,
            )
            credentials = Token(token.get("access_token", ""))

        self._client = CogniteClient(
            ClientConfig(
                client_name=client_name,
                base_url=os.environ["CDF_URL"],
                project=os.environ["CDF_PROJECT"],
                credentials=credentials,
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
                "example must be set to one of the values in the inventory.json file used by CDFToolConfig()."
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
            resp = self.client.iam.token.inspect()
            if resp is None or len(resp.capabilities) == 0:
                raise CogniteAuthError(
                    f"Don't have any access rights. Check credentials."
                )
        except Exception as e:
            raise e
        # iterate over all the capabilties we need
        for cap, actions in capabilities.items():
            # Find the right capability in our granted capabilities
            for k in resp.capabilities:
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
            raise CogniteAuthError(
                f"Don't have correct access rights. Need READ and WRITE on datasetsAcl."
            )
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
            raise CogniteAuthError(
                f"Don't have correct access rights. Need also WRITE on "
                + "datasetsAcl or that the data set {get_dataset_name()} has been created."
            )
