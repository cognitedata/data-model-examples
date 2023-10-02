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
import os

from utils import ToolGlobals

from utils import *

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: ./dump_datamodel.py <space|all|global> <data_model|all> <directory>"
        )
        exit(1)
    if not os.path.exists(sys.argv[3]):
        os.makedirs(sys.argv[3])
    if sys.argv[1] in ["all", "global"]:
        if sys.argv[1] == "global":
            include_global = True
        else:
            include_global = False
        if sys.argv[2] == "all":
            model_name = None
        else:
            model_name = sys.argv[2]
        dump_datamodels_all(
            ToolGlobals,
            target_dir=sys.argv[3],
            model_name=model_name,
            include_global=include_global,
        )
        exit(0)
    dump_datamodel(
        ToolGlobals,
        space_name=sys.argv[1],
        model_name=sys.argv[2],
        target_dir=sys.argv[3],
    )
