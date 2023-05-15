#!/bin/bash
source ../.env
echo "Logging into CDF using environment variables from .env..."
cdf login --client-id=$CDF_CLIENT_ID --client-secret=$CDF_CLIENT_SECRET --tenant=$CDF_TENANT_ID --cluster=$CDF_CLUSTER $CDF_PROJECT
cdf status