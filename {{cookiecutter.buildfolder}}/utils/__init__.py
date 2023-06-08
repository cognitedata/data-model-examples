import sys
import logging
from dotenv import load_dotenv
from .utils import CDFToolConfig

"""Makes ToolGlobals available
"""

logger = logging.getLogger(__name__)

gettrace = sys.gettrace()
debug_status = True if gettrace else False
# Load .env in current folder
load_dotenv()
if debug_status:
    logger.warning("WARNING!!!! Debugging is active. Using .env from repo root.")
    # If you debug within the {{cookiecutter.buildfolder}}, you will already have a .env file as a template there (git controlled).
    # Rather use .env from the repo root (git ignored)
    # Override...
    load_dotenv("../.env")
    ToolGlobals = CDFToolConfig(
        {
            "movie_actors": {
                "raw_db": "test_movies",
                "data_set": "tutorial_movies_dataset",
                "model_space": "tutorial_movies",
                "data_model": "tutorial_MovieDM",
            },
            "apm_simple": {
                "raw_db": "test_apm_simple",
                "data_set": "Valhall_System_23",
                "model_space": "tutorial_apm_simple",
                "data_model": "tutorial_apm_simple",
            },
        }
    )
else:
    # ToolGlobals is a singleton that is loaded once as this is a python module
    ToolGlobals = CDFToolConfig()
