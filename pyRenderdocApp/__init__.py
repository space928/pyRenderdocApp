#  Copyright (c) 2024 Thomas Mathieson.
#  Distributed under the terms of the MIT license.
from ctypes import *
import sys
if sys.version_info >= (3, 9):
    from importlib.resources import files  # type: ignore
else:
    from importlib.resources import path
from .renderdoc_api import RENDERDOC_API_1_6_0
from typing import Optional


def load_render_doc(renderdoc_path: Optional[str] = None) -> RENDERDOC_API_1_6_0:
    """
    Loads the Renderdoc in-app library.

    :param renderdoc_path: optionally, a path to a local copy of the Renderdoc library. Must be compatible with the
                           current platform.
    :return: the loaded instance of the Renderdoc API.
    """
    if renderdoc_path is None:
        if sys.platform.startswith("win32"):
            is_64bits = sys.maxsize > 2 ** 32
            if is_64bits:
                lib_path = "renderdoc_64.dll"
            else:
                lib_path = "renderdoc.dll"
        elif sys.platform.startswith("linux"):
            lib_path = "librenderdoc.so"
        else:
            raise NotImplementedError(f"Operating system '{sys.platform}' is not supported!")

        try:
            if sys.version_info >= (3, 9):
                lib_path = str(files("pyRenderdocApp.lib").joinpath(lib_path))
            else:
                with path("pyRenderdocApp.lib", lib_path) as p:
                    lib_path = str(p.absolute())
        except Exception as e:
            raise FileNotFoundError("Couldn't load renderdoc library!")

        # find_library("renderdoc")
        if lib_path is None:
            raise FileNotFoundError("Couldn't load renderdoc library!")
    else:
        lib_path = renderdoc_path

    rd = CDLL(lib_path)
    return RENDERDOC_API_1_6_0(rd)
