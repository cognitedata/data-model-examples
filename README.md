# Cognite Data Fusion Data Model Examples

This repository contains examples of how to work with data models in Cognite Data Fusion.

See [Changelog](./CHANGELOG.md) for recent changes.

The code is licensed under the [Apache License 2.0](LICENSE.code.md), while the documentation and methods are licensed
under [Creative Commons](LICENSE.docs.md). Each of the example data sets have their own license,

see the LICENSE.dataset.md in each examples directory.

## Set up of the CDF project and credentials

> If you want to sign up for a trial project, go to <https://developer.cognite.com/signup>.

The default configuration here has been adapted to these trial projects. The default identity provider (IDP)
URLs and IDP_CLIENT_ID are all set up to use the Cognite trial project identity provider.
The only settings you need
to change when running `cookiecutter` (see below) are the CDF_PROJECT, IDP_CLIENT_ID, and the IDP_CLIENT_SECRET.
Your trial project starts with `trial-` and then a sequence of numbers and
letters. You can find the project name in the email you received when you signed up for the trial project
or in the URL in your browser when you log into <https://cog-trials.fusion.cognite.com>.
The client credentials were also forwarded to you in the trial project welcome email.

If you are using a standard CDF project and not a trial project, you should change the IDP_* settings to
match your project's identity provider settings. E.g. if you use Microsoft Active Directory, the
IDP_TOKEN_URL setting should be in the format:
`"https://login.microsoftonline.com/{{cookiecutter.IDP_TENANT_ID}}/oauth2/v2.0/token"`

**If you don't have a project and you are a customer or partner, you get the CDF project
from <support@cognite.com>.**

See [README.me](./{{cookiecutter.buildfolder}}/README.md) for details on permissions needed. If you are using
a trial project, all the permissions have already been set up for you in the basic_access group in your project.

## Getting Started by using cookiecutter

The easiest way to use this repo is not to check it out, but rather use cookiecutter to make a local copy:

```bash
pip install cookiecutter
cookiecutter https://github.com/cognitedata/data-model-examples.git
```

You will be prompted to supply your credentials for a CDF project (you need client credentials, so a client
id and a client secret).

The minimum you need to configure is the following (IDP = Identity Provider, typically Azure Active Directory):

* CDF_CLUSTER (the prefix before cognitedata.com)
* CDF_PROJECT (your CDF project name)
* IDP_TENANT_ID (the tenant id for the CDF project in your identity provider, for Azure this can be .something.onmicrosft.com)
* IDP_CLIENT_ID (the client id for the service principal/service account you have set up in your IDP)
* IDP_CLIENT_SECRET (the client secret for the service principal/service account you have set up in your IDP)

The remaining configurations are optional, but you will be prompted for them, so just press enter if you do not
need to change them.

**The prefix tells you where you get the information from: CDF_* is for your CDF project, while IDP_* is for your
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
