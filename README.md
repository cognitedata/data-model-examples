# Cognite Data Fusion Data Model Examples
This repository contains examples on how to work with data models in Cognite Data Fusion.

## Setup
1. Install [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) and [pip](https://packaging.python.org/en/latest/tutorials/installing-packages/) if you do not already have them.
2. Install the data modeling cli tool:
    ```
    npm install -g @cognite/cdf-cli
    ```
3. Install the transformations cli tool:
    ```
    pip install cognite-transformations-cli
    ```
4. Clone this repository
    ```
    git clone https://github.com/cognitedata/data-model-examples.git
    ```
5. Authenticate with the data modeling cli tool
    ```
    cdf login
    ```
Here you need to fill in the project (e.g. `cognite`), which cluster (e.g. `westeurope-1`) and Azure AD tenant (e.g. `cognite.onmicrosoft.com`).

## How to run an example
1. Change directory to one of the example folders, e.g. `guides/introduction`
