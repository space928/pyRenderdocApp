# pyRenderdocApp
A small wrapper for the renderdoc in-app api in python.

This project wraps the methods exposed by `renderdoc_app.h` with the python ctypes API. It's designed to closely match 
the official API, with the main difference being that the function and parameter names have been converted to snake case
(ie: `GetAPIVersion()` --> `get_api_version()`). The original doc comments from `renderdoc_app.h` have also been ported 
over (and modified where appropriate). For more information about using the Renderdoc in-app API, read the official 
documentation: https://renderdoc.org/docs/in_application_api.html

## Installing

Install with `pip`:
```bash
pip install pyRenderdocApp
```

The package includes renderdoc binaries for Windows and Mac.
