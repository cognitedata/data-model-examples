#/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cdf dm create --interactive false --external-id {{cookiecutter.apm_simple_datamodel}} --space {{cookiecutter.apm_simple_space}} {{cookiecutter.apm_simple_datamodel}}
cdf dm publish --interactive false --external-id {{cookiecutter.apm_simple_datamodel}} --space {{cookiecutter.apm_simple_space}} --version 1 --file $SCRIPT_DIR/datamodel.graphql