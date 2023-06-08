# The utils directory

The transformation*.py files and load_yaml.py file are all from the transformations_cli tool.
They are loaded here to avoid having to install the transformations_cli tool and to avoid
dependency mismatch between different versions of the CDF SDK.

The utils.py and __init__.py files defines ToolGlobals, a single object instance (singleton)
that gives you simple access to the CDF API client and an ACL verification tool.

See docs of CDFToolConfig (defined in utils.py) for more information.
