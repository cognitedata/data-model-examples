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

from utils import dump_transformations

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ./dump_transformations.py t1,t2,t3... <directory>")
        exit(1)
    if not os.path.exists(sys.argv[2]):
        os.makedirs(sys.argv[2])
    if sys.argv[1] == "all":
        ts = None
    else:
        ts = sys.argv[1].split(",")
    dump_transformations(
        ToolGlobals,
        external_ids=ts,
        target_dir=sys.argv[2],
    )
