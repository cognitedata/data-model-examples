# Cognite Data Fusion Data Model Examples

This repository contains examples of how to work with data models in Cognite Data Fusion.

See [Changelog](./CHANGELOG.md) for recent changes.

The code is licensed under the [Apache License 2.0](LICENSE.code.md), while the documentation and methods are licensed
under [Creative Commons](LICENSE.docs.md). Each of the example data sets have their own license,

see the LICENSE.dataset.md in each examples directory.

## Set up of the CDF project and credentials

> To sign up for a trial project, go to <https://developer.cognite.com/signup>.

The default configuration here has been adapted to these trial projects. The default identity provider (IDP)
URLs and IDP_CLIENT_ID are all set up to use the Cognite trial project identity provider.
The only settings you need
to change when running `cookiecutter` (see below) are `CDF_PROJECT`, `IDP_CLIENT_ID`, and `IDP_CLIENT_SECRET`.
Your trial project starts with `trial-` and then a sequence of numbers and
letters. You can find the project name in the email you received when you signed up for the trial project
or in the URL in your browser when you sign in <https://cog-trials.fusion.cognite.com>.
You will also have the client credentials in the trial project welcome email.

If you use a standard CDF project and not a trial project, you should change the IDP_* settings to
match your project's identity provider settings. E.g. if you use Microsoft Active Directory, the
IDP_TOKEN_URL setting should be in the format:
`"https://login.microsoftonline.com/{{cookiecutter.IDP_TENANT_ID}}/oauth2/v2.0/token"`.

**If you don't have a project and you are a customer or partner, you can get the CDF project from <support@cognite.com>.**

See [README.me](./{{cookiecutter.buildfolder}}/README.md) for the details on permissions required. If you are using
a trial project, all the permissions have already been set up for you in the basic_access group in your project.

## Get started using cookiecutter

The easiest way to use this repo is not to check it out but rather use cookiecutter to make a local copy:

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

When you do `import utils`, the code in `__init__.py` will execute and give you a pre-initiated
ToolGlobals object. This object has a .client pre-configured CDF API client that you can
use to call all the functions in the Cognite Python SDK. It will try to load the .env file
with the credentials you have set up (either using cookiecutter or manually set the values in the .env
file). It also detects if you are debugging, and if so, it will use the .env file in the root of the repo,
not the one in the `{{cookicutter.buildfolder}}` (as that one is a template).

So, ToolGlobals gives you a pre-configured CDF API client, a set of configuration attributes you can use
in your app (and used by the utils/ functions), as well as a simple way of loading and deleting data sets
using the utils/ functions. You simply set the example directory where your data is stored by setting
`ToolGlobals.example="folder_name"` and there should be an entry in inventory.json configuring
the data set, raw database, etc used when loading and deleting the data set.

If you want to use the code from this repo for your own project, you can copy the utils/ directory
and the inventory.json file to your own project, edit inventory.json with an entry for your project
and do `import utils`. If you don't need config variables or load/delete data sets, you can create your
own ToolGlobals for calling the CDF API client by either explicitly setting the config to an empty dict
or deleting inventory.json:

```python
import utils
ToolGlobals = CDFToolConfig(client_name="name_of_your_app", config={})
ToolGlobals.client.raw.tables.list("raw_db_name")
```

If inventory.json is not present and you don't supply an empty config, all the variables will be set to `default`.
The configuration attributes are only used by the functions found in utils/, not the CDF SDK client.

[CONTRIBUTING.md](./CONTRIBUTING.md) explains more about how the data sets are set up.

And finally, if you just want to get inspired and copy some code to configure your own CDF SDK client, `utils/utils.py`
in `{{cookiecutter.buildfolder}}` is a good place to start.

## Contributing to this template repository

See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to contribute to the templates or new examples.
