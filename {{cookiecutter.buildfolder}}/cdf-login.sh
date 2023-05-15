#!/bin/bash
# Use set -a to automatically export all variables
# This will not be persisted in your own shell, just to the commands run by this script
# Use set -a; source .env; set +a
# from your command line to load the variables into your current shell.
set -a 
source ../.env
set +a
echo "Logging into CDF using environment variables from .env..."
cdf login --client-id=$CDF_CLIENT_ID --client-secret=$CDF_CLIENT_SECRET --tenant=$CDF_TENANT_ID --cluster=$CDF_CLUSTER $CDF_PROJECT
cdf status

echo "Testing by listing transformstions..."
# This will also work when .env variables are loaded: transformations-cli list
transformations-cli --token-url=$CDF_TOKEN_URL --client-secret=$CDF_CLIENT_SECRET --client-id=$CDF_CLIENT_ID --scopes=$CDF_SCOPES --cluster=$CDF_CLUSTER --cdf-project-name=$CDF_PROJECT list
