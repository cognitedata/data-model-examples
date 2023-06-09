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

#/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cdf dm create --interactive false --external-id {{cookiecutter.movie_actors_datamodel}} --space {{cookiecutter.movie_actors_space}} {{cookiecutter.movie_actors_datamodel}}
cdf dm publish --interactive false --external-id {{cookiecutter.movie_actors_datamodel}} --space {{cookiecutter.movie_actors_space}} --version 1 --file $SCRIPT_DIR/datamodel.graphql