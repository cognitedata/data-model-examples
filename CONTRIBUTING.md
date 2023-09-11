# CONTRIBUTING

This repo uses [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) to manage examples
as templates. If checking out this repo, you can build the examples with your settings in an interactive way
by installing cookiecutter and running `cookiecutter .`.
Cookiecutter will store config files for you in `~/.cookiecutter`.

## The structure of an example

Each example should have a README.md file that introduces the data set and how
to use it. You should also include a LICENSE.dataset.md file to clearly articulate the terms
the data set is licensed under.

You can use `./examples/apm_simple/` directory as a reference for how to set up your own example.
The structure should be the following under the `examples/` directory:

* make a folder with the name of the example. This name is used throughout as a reference for
    the example.
* put all the data in the `data` directory with each data type in a sub-directory.
* YAML config files for transformations should be in the `transformations` directory. These are exported easily
    from each transformation in the `Integrate - Transform Data` meny in the Fusion UI (`CLI Manifest``).
* a `datamodel.graphql` file with the CDF data model to load should be in the root
    of the example directory. This is exported from your data model in the Fusion UI visual data modeling editor.

## To add a new example

1. Follow the structure of the existing ones and add a new one in a separate directory.
1. Edit the cookiecutter.json file to add the defaults for your example:

    ```json
    "apm_simple_raw_db": "tutorial_apm",
    "apm_simple_datamodel": "tutorial_apm_simple",
    "apm_simple_space": "tutorial_apm_simple",
    "apm_simple_data_set": "Valhall_System_23",
    "apm_simple_data_set_desc": "Valhall_System_23"
    ```

1. Then edit inventory.json to add your example to the list so that the scripts can pick up
    the example. Note that the cookiecutter variables allow the user to substitute with their own values when using the template.

1. Edit the README.md in this folder (at the end) with a short description of the example.

1. You should be good to go. Run `cookiecutter .` to generate the build directory, now with your example.

1. Update the [Changelog](./CHANGELOG.md)

1. Once it's working, open a Pull Request on this repo.

1. Thanks a lot!!!

### A note on the data_model json files

> The scripts will default load the `datamodel.graphql`. The json files in the `data_model` directory
> are not used unless you use the `load_datamodel_dump()` function in `load_data.py` in utils/.
> This function is used by `restore_datamodel.py`.

The json files found in the data_model folder are basically a dump of the data model in CDF.
You can use the `dump_datamodel.py` script (see below) to dump the data model from a CDF tenant in this format.

## Debugging python scripts

The cookiecutter template variables can make it harder to debug. To simplify debugging of
Python scripts and allow you to debug the files (like load_data.py) directly in an IDE,
do the following:

1. Copy your own .env file into the **root folder** of this repo (where this file lives).
2. Bypass the inventory.json file by using a debug hardcoded configuration for your example in
    `utils/__init__.py` (see below how)
3. If you use Visual Studio Code, debug configurations can be found in `.vscode/launch.json`
4. Start debugging the regular way. The debug status will be picked up and the config and .env file will be overridden.

You can see how the examples_config dict is overridden and loads the root .env instead of the .env
in the `{{cookiecutter.buildfolder}}/utils/__init__.py` file:

```python
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
```

## Alternative way to run if you clone the repo

1. Edit temporary `cookiecutter.json` with your real values (not template values)
2. Run `cookiecutter --no-input .`
3. You will find the built examples in either `./build` or the folder you specified
4. **Don't check in the modified cookiecutter.json!!**

## When developing examples

You can also run `cookiecutter --replay .` This is very useful if you are editing the templates in `{{cookiecutter.buildfolder}}`.

## dump_datamodel.py

The `dump_datamodel.py` script is used to dump the data model from a Cognite Data Fusion tenant. It takes
four arguments: <space> <model_name> <version> <target_dir>. You should dump it to a directory called
`data_model` under examples/<your_model>/.

If you then use the script `restore_datamodel.py <your_model>` to load the data model, you have
basically done a backup and restore of the data model. Please note that the data model dump (json files) is
not used default by the CLI tool to load the data model.

## Deploying the repo

This repo does not have a CI/CD pipeline, so merging to main will make the changes immediately available
to users who use cookiecutter.

When changing the examples and utils directories, a Cognite engineer should update these two directories
for the JupyterLite notebooks in Fusion UI (the dshublite private repo).
It is a direct copy of the files in this repo with
a CI/CD pipeline to deploy a new version of JupyterLite.
