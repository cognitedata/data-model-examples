#!/bin/bash

# Copyright 2023 Gognite AS
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

# Use set -a to automatically export all variables
# This will not be persisted in your own shell, just to the commands run by this script
# Use set -a; source .env; set +a
# from your command line to load the variables into your current shell.
set -a 
source ./.env
set +a
echo "Logging into CDF using environment variables from .env..."
cdf login --client-id=$IDP_CLIENT_ID --client-secret=$IDP_CLIENT_SECRET --tenant=$IDP_TENANT_ID --cluster=$CDF_CLUSTER $CDF_PROJECT
cdf status

echo "Testing by listing transformations..."
# This will also work when .env variables are loaded: transformations-cli list
transformations-cli --token-url=$IDP_TOKEN_URL --client-secret=$IDP_CLIENT_SECRET --client-id=$IDP_CLIENT_ID --scopes=$IDP_SCOPES --cluster=$CDF_CLUSTER --cdf-project-name=$CDF_PROJECT list
