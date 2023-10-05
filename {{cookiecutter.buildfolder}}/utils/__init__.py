from .utils import CDFToolConfig
from .load_yaml import load_yaml
from .transformations_config import parse_transformation_configs
from .transformations_api import (
    to_transformation,
    get_existing_transformation_ext_ids,
    get_new_transformation_ids,
    upsert_transformations,
)
from .load import (
    load_files,
    load_raw,
    load_timeseries,
    load_timeseries_datapoints,
    load_timeseries_metadata,
    load_transformations,
    load_readwrite_group,
)
from .delete import (
    delete_datamodel,
    delete_files,
    delete_raw,
    delete_timeseries,
    delete_transformations,
)

from .datamodel import (
    load_datamodel,
    load_datamodel_dump,
    describe_datamodel,
    dump_datamodel,
    dump_datamodels_all,
    clean_out_datamodels,
)

from .transformations import (
    run_transformations,
    dump_transformations,
    load_transformations_dump,
)

import sys
import os
import logging

"""Makes ToolGlobals available as a singleton to all modules in the package.
"""

logger = logging.getLogger(__name__)
# TODO Change this to a name for your client
_client_name = "Cognite examples library"
_debug_status = True if sys.gettrace() else False

_envfile = (
    True
    if (
        (_debug_status and os.path.isfile("../.env"))
        or (not _debug_status and os.path.isfile(".env"))
    )
    else False
)
_jupyter = True if ("CDF_URL" not in os.environ and not _envfile) else False

# Load .env
if _envfile and not _jupyter:
    from dotenv import load_dotenv

    if _debug_status:
        # If you debug within the {{cookiecutter.buildfolder}}, you will already have a .env file as a template there (git controlled).
        # Rather use .env from the repo root (git ignored)
        # Override...
        load_dotenv("../.env")
    else:
        load_dotenv()
if _debug_status or _jupyter:
    if _debug_status:
        logger.warning("WARNING!!!! Debugging is active. Using .env from repo root.")
    ToolGlobals = CDFToolConfig(
        client_name=_client_name,
        config={
            "movie_actors": {
                "raw_db": "tutorial_movies",
                "data_set": "tutorial_movies",
                "data_set_desc": "Data set for the movies-actor tutorial",
                "model_space": "tutorial_movies",
                "data_model": "tutorial_MovieDM",
            },
            "apm_simple": {
                "raw_db": "tutorial_apm",
                "data_set": "Valhall_System_23",
                "data_set_desc": "Valhall_System_23",
                "model_space": "tutorial_apm_simple",
                "data_model": "tutorial_apm_simple",
            },
        },
    )
else:
    # ToolGlobals is a singleton that is loaded once as this is a python module
    ToolGlobals = CDFToolConfig(client_name=_client_name)
