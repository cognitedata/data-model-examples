# CONTRIBUTING

This repo uses [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) to manage examples
as templates. If checking out this repo, you can build the examples with your settings in an interactive way
by installing cookiecutter and running `cookiecutter .`.
Cookiecutter will store config files for you in `~/.cookiecutter`.

## The structure of an example

Each example should have a README.md file that introduces the data set and how
to use it. You should also include a LICENSE.dataset.md file to clearly articlate the terms
the data set is licensed under.

You can use `./examples/apm_simple/` directory as a reference for how to set up your own example.
The structure should be the following under the `examples/` directory:

* make a folder with the name of the example. This name is used throughout as a reference for
    the example.
* put all the data in the `data` directory with each data type in a sub-directory.
* yaml config files for transformations should be in the `transformations` directory
* a datamodel.graphql file with the CDF data model to load should be in the root
    of the example directory
* Copy and adapt the scripts in e.g. `apm_simple` directory.

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

3. Then edit inventory.json to add your example to the list so that the scripts can pick up
    the example. Note that the cookiecutter variables allow the user to substitute with their own values when using the template.

4. Edit the README.md in this folder (at the end) with a short description of the example.

5. You should be good to go. Run `cookiecutter .` to generate the build directory, now with your example.

6. Update the [Changelog](./CHANGELOG.md)

7. Once it's working, open a Pull Request on this repo.

8. Thanks a lot!!!

## Debugging python scripts

The cookiecutter template variables can make it harder to debug. To simplify debugging of
python scripts and allow you to debug the files (like load_data.py) directly in an IDE,
do the following:

1. Copy your own .env file into the **root folder** of this repo (where this file lives).
2. Bypass the inventory.json file by using a debug hardcoded configuration for your example in
    `utils/__init__.py` (see below how)
3. If you use Visual Studio Code, debug configurations can be found in `.vscode/launch.json`
4. Start debugging the regular way. The debug status will be picked up and the config and .enf file will be overridden.

You can see how the examples_config dict is overridden and loads the root .env instead of the .env
in the `{{cookiecutter.buildfolder}}/utils/__init__.py` file:

```python
# Load .env in current folder
load_dotenv()
if debug_status:
    logger.warning("WARNING!!!! Debugging is active. Using .env from repo root.")
    # If you debug within the {{cookiecutter.buildfolder}}, you will already have a .env file as a template there (git controlled).
    # Rather use .env from the repo root (git ignored)
    # Override...
    load_dotenv("../.env")
    ToolGlobals = CDFToolConfig(
        client_name=client_name,
        config={
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
        },
    )
else:
    # ToolGlobals is a singleton that is loaded once as this is a python module
    ToolGlobals = CDFToolConfig(client_name=client_name)
```

## Alternative way to run if you clone the repo

1. Edit temporary `cookiecutter.json` with your real values (not template values)
2. Run `cookiecutter --no-input .`
3. You will find the built examples in either `./build` or the folder you specified
4. **Don't check in the modified cookiecutter.json!!**

## When developing examples

You can also run `cookiecutter --replay .` This is very useful if you are editing the templates in `{{cookiecutter.buildfolder}}`.
