# CONTRIBUTING

This repo uses [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) to manage examples
as templates. If checking out this repo, you can build the examples with your settings in an interactive way
by installing cookiecutter and run `cookiecutter .`.
Cookiecutter will store config files for you in `~/.cookiecutter`.

## The structure of an example

Each example should have a README.md file that introduces the data set and how
to use it.

The structure should be the following:

* all data in the `data` directory with each data type in a sub-directory
* yaml config files for transformations in the `transformations` directory
* a datamodel.graphql file with the CDF data model to load
* Copy and adapt the scripts in e.g. `apm_simple` directory

## To add a new example

1. Follow the structure of the existing ones and add a new in a separate directory.
2. Edit the cookiecutter.json file to add the defaults for your example:

    ```json
    "apm_simple_raw_db": "tutorial_oid",
    "apm_simple_datamodel": "tutorial_apm_simple",
    "apm_simple_space": "tutorial_apm_simple",
    "apm_simple_data_set": "Valhall_System_23",
    "apm_simple_data_set_desc": "Valhall_System_23"
    ```

3. Then edit inventory.json to add your example to the list so that the load_data-py script can pick up the example.

4. Edit README.md at the end to describe the example.

5. You should be good to go. Run `cookiecutter .` to generate the build directory, now with your example.

6. Once it's working, open a Pull Request on this repo.

7. Thanks a lot!!!

## Debugging python scripts

To simplify debugging of python scripts for templates, a couple of things should be done:

1. Use your own .env file in the **root folder** of this repo.
2. Bypass the inventory.josn file by using a debug hardcoded configuration (see below how)

You can see how `load_data.py` overrides the examples_config dict and loads the root .env instead of the .env
in the `{{cookiecutter.buildfolder}}`folder:

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

## Alternative way to run when you check out the repo

1. Edit `cookiecutter.json` with your values (not template values)
2. Run `cookiecutter --no-input .`
3. You will find the built examples in either `./build` or the folder you specified

**Don't check in the modified cookiecutter.json!!**

## When developing examples

You can also run `cookiecutter --replay .` This is very useful if you are editing the templates in `{{cookicutter.buildfolder}}`.
