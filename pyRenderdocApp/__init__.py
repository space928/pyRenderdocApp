#  Copyright (c) 2023 Thomas Mathieson.
#  Distributed under the terms of the MIT license.

from ctypes import *
import sys
from .renderdoc_api import RENDERDOC_API_1_6_0


def load_render_doc() -> RENDERDOC_API_1_6_0:
    if sys.platform.startswith("win32"):
        is_64bits = sys.maxsize > 2 ** 32
        if is_64bits:
            lib_path = "lib/renderdoc_64.dll"
        else:
            lib_path = "lib/renderdoc.dll"
    elif sys.platform.startswith("linux"):
        lib_path = "lib/librenderdoc.so"
    else:
        raise NotImplementedError(f"Operating system '{sys.platform}' is not supported!")
    # find_library("renderdoc")
    if lib_path is None:
        raise FileNotFoundError("Couldn't load renderdoc library!")

    rd = CDLL(lib_path)
    return RENDERDOC_API_1_6_0(rd)
