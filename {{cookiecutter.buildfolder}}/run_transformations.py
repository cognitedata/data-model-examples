#!/usr/bin/env python

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

import sys
from utils import ToolGlobals
from utils.transformations_config import parse_transformation_configs


if __name__ == "__main__":
    ToolGlobals.example = sys.argv[1]
    client = ToolGlobals.verify_client(
        capabilities={"transformationsAcl": ["READ", "WRITE"]}
    )
    configs = parse_transformation_configs(
        f"./examples/{ToolGlobals.example}/transformations/"
    )
    transformations_ext_ids = [t.external_id for t in configs.values()]
    try:
        for t in transformations_ext_ids:
            client.transformations.run(transformation_external_id=t, wait=False)
        print(
            f"Started {len(transformations_ext_ids)} transformation jobs for example {ToolGlobals.example}."
        )
    except Exception as e:
        print(
            f"Failed to start transformation jobs for example {ToolGlobals.example}. They may not exist."
        )
        print(e)
        exit(1)
