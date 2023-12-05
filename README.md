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

## Example

Here's what the example from the RenderDoc documentation ([link](https://renderdoc.org/docs/in_application_api.html#_CPPv416RENDERDOC_GetAPI17RENDERDOC_VersionPPv)) would look like in python:
```py
from pyRenderdocApp import load_render_doc
from ctypes import c_void_p

# At init, load the renderdoc api
rdoc_api = load_render_doc()

# To start a frame capture, call StartFrameCapture.
# You can specify None, None for the device to capture on if you have only one device and
# either no windows at all or only one window, and it will capture from that device.
# See the documentation for a longer explanation
rdoc_api.start_frame_capture(c_void_p(0), c_void_p(0))

# Your rendering should happen here

# Stop the capture
rdoc_api.end_frame_capture(c_void_p(0), c_void_p(0))
```

## Building

Build using `build`:
```bash
pip install build twine hatch
```

Build the wheel:
```bash
python -m build
```

Then to upload the package to PyPI, do:
```bash
twine upload dist/pyrenderdocapp*
```
