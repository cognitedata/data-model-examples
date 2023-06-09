# Cognite Data Fusion Data Model Examples

This repository contains examples on how to work with data models in Cognite Data Fusion.

The code is licensed under the [Apache License 2.0](LICENSE.code.md), while the documentation and methods are licensed
under [Creative Commons](LICENSE.docs.md). Each of the example data sets have their own license,
see the LICENSE.dataset.md in each examples directory.

## Set up the CDF project and get credentials

**You need a CDF project and client credentials for a service account/principal that has access to the project
through a CDF access group (see below for needed permissions). You get the CDF project from
<support@cognite.com> and you configure the service principal/account in the identity provider (e.g. Azure Active Directory)
that the CDF project has been configured to use.**

See the python SDK [intro doc](https://developer.cognite.com/dev/guides/sdk/python/python_auth_oidc/) for how to get the credentials.

See [README.me](./{{cookiecutter.buildfolder}}/README.md) for details on permissions needed.

## Getting Started by using cookiecutter

The easiest way to use this repo is not to check it out, but rather use cookiecutter to make a local copy:

```bash
pip install cookiecutter
cookiecutter https://github.com/cognitedata/data-model-examples.git
```

You will be prompted to supply your credentials for a CDF project (you need client credentials, so a client
id and a client secret).

The minimum you need to configure are the following (IDP = Identity Provider, typically Azure Active Directory):

* CDF_CLUSTER (the prefix before cognitedata.com)
* CDF_PROJECT (your CDF project name)
* IDP_TENANT_ID (the tenant id for the CDF project in your identity provider, for Azure this can be .something.onmicrosft.com)
* IDP_CLIENT_ID (the client id for the service principal/service account you have set up in your IDP)
* IDP_CLIENT_SECRET (the client secret for the service principal/service account you have set up in your IDP)

The remaining configurations are optional, but you will be prompted for them, so just press enter if you do not
need to change them.

**The prefix tells you were you get the information from: CDF_* is for your CDF project, while IDP_* is from your
identity provider.**

You will get a `./build` folder (unless you change the default) that contains the examples configured and ready
for your CDF project!

Cookiecutter will store your configurations in `~/.cookiecutter_replay/`, so you can update the build folder
by running `cookiecutter --replay https://github.com/cognitedata/data-model-examples.git`

## How to use the examples after using cookiecutter

See the README.md in the build folder for how to use the examples.
Before using cookiecutter, this file is [README.me](./{{cookiecutter.buildfolder}}/README.md).

## Use this template tool for your own data

If you want to create your own data set that you can load and delete at will, you can create
your own example. Just follow the guidelines below on how to contribute to this repository, but
just skip submitting your example as a pull request.

## Contributing to this template repository

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to contribute to the templates or new examples.
