# To add a new example, add a new entry here with the same name as the folder
# These values are used by the python scripts.
examples_config = {
    "movie_actors": {
        "raw_db": "{{cookiecutter.movie_actors_raw_db}}",
        "raw_db_key": "id",
    },
    "apm_simple": {"raw_db": "{{cookiecutter.apm_simple_raw_db}}", "raw_db_key": "key"},
}
