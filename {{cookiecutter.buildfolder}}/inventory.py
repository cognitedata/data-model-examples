# To add a new example, add a new entry here with the same name as the folder
# These values are used by the python scripts.
class ExamplesConfig:
    """Configurations for how to store data in CDF

    To add a new example, add a new entry here with the same name as the folder.
    These values are used by the python scripts.
    """

    def __init__(self, config: dict | None = None) -> None:
        if config is not None:
            self._config = config
        else:
            self._config = {
                "movie_actors": {
                    "raw_db": "{{cookiecutter.movie_actors_raw_db}}",
                    "data_set": "{{cookiecutter.movie_actors_data_set}}",
                },
                "apm_simple": {
                    "raw_db": "{{cookiecutter.apm_simple_raw_db}}",
                    "data_set": "{{cookiecutter.apm_simple_data_set}}",
                },
            }

    def get(self, example: str, attr: str) -> str:
        return self._config.get(example, {}).get(attr, "")
