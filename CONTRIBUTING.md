# CONTRIBUTING

This repo uses [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) to manage examples
as templates. If checking out this repo, you can build the examples with your settings in an interactive way
by installing cookiecutter and run `cookiecutter .` or
you can edit the `./{{cookiecutter.buildfolder}}/cookiecutter.json` file and then just run `./build.sh`. Either
way, cookiecutter will store config files for you in `~/.cookiecutter`.

To add a new example:

1. Follow the structure of the existing ones and add a new.
2. Edit the cookiecutter.json file to add the defaults for your example:

    ```json
        "apm_simple_raw_db": "oid",
        "apm_simple_datamodel": "apm_simple",
        "apm_simple_space": "apm_simple"
    ```

3. Then edit inventory.py with the basic information about the example, so that the scripts can pick it up.

## Debugging python scripts

To simplify debugging of python scripts for templates, a couple of things should be done:

1. Use your own .env file in the root folder of this repo.
2. Bypass the inventory.py file a debug hardcoded configuration (see below how)

You can see how `load_data.py` overrides the examples_config and loads the root .env instead of the .env
in the `{{cookiecutter.buildfolder}}`folder (which uses template variables that are not set):

```python
if debug_status:
    load_dotenv("../.env")
    examples_config = {
        "movie_actors": {
            "raw_db": "test_movies",
        },
        "apm_simple": {
            "raw_db": "test_apm_simple",
        },
    }
else:
    load_dotenv()
```

## How to run an example without checking out repo

1. Run `cookiecutter .` or `cookiecutter https://github.com/cognitedata/data-model-examples.git`
2. Change directory to `./build/<example-to-use>`
3. Check out the README.md file

## Alternative way to run when you check out the repo

1. Edit `cookiecutter.json` with your defaults
2. Run `cookiecutter --no-input .`
3. You will find the built examples in either `./build` or the folder you specified

## When developing examples

You can also run `cookiecutter --replay .` This is very useful if you are editing the templates in `{{cookicutter.buildfolder}}`.
