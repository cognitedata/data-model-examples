#!/bin/bash
export TRANSFORMATIONS_CLIENT_ID=myclientid
export TRANSFORMATIONS_CLIENT_SECRET=myclientsecret
export TRANSFORMATIONS_TOKEN_URL=https://login.microsoftonline.com/{AzureAdTenantId}/oauth2/v2.0/token
export TRANSFORMATIONS_SCOPES="https://westeurope-1.cognitedata.com/.default"
export TRANSFORMATIONS_AUDIENCE=https://westeurope-1.cognitedata.com # might be optional
export TRANSFORMATIONS_PROJECT=mycdfproject
export TRANSFORMATIONS_CLUSTER=westeurope-1