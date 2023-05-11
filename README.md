# Cognite Data Fusion Data Model Examples

This repository contains examples on how to work with data models in Cognite Data Fusion.

## Setup

This repo uses [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/index.html) to manage examples.
You can build the examples with your settings in an interactive way by installing cookiecutter and run `cookiecutter ./guides` or
you can edit the `./guides/cookiecutter.json` file and then just run `./build.sh`. Either way, cookiecutter will story config
files for you in `~/.cookiecutter`.

0. To install the requirements for cookiecutter, you can either use `pip install -r requirements.txt` or use the supplied `pyproject.
toml` file and poetry (if you prefer).

1. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) if you do not already have them.

2. Install the data modeling cli tool:

    ```bash
    npm install -g @cognite/cdf-cli
    ```

3. Install the transformations cli tool:

    ```bash
    pip install cognite-transformations-cli
    ```

4. Clone this repository

    ```bash
    git clone https://github.com/cognitedata/data-model-examples.git
    ```

5. Authenticate with the data modeling cli tool

    ```bash
    cdf login
    ```

Here you need to fill in the project (e.g. `cognite`), which cluster (e.g. `westeurope-1`) and Azure AD tenant (e.g. `cognite.onmicrosoft.com`).

## How to run an example

1. Edit `.guides/cookiecutter.json`
2. Run `./build.sh`
3. Change directory to `./build/<example-to-use>`
4. Check out the README.md file
