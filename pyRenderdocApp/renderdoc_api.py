#  Copyright (c) 2023 Thomas Mathieson.
#  Distributed under the terms of the MIT license.
# Ported from renderdoc_app.h, available under the MIT license Copyright (c) 2019-2023 Baldur Karlsson
# https://github.com/baldurk/renderdoc/blob/v1.x/renderdoc/api/app/renderdoc_app.h

from ctypes import *
from .renderdoc_enums import *


class RENDERDOC_API_1_6_0:
    """
    RenderDoc API v1.6.0 wrapper. Documentation available at:
    https://renderdoc.org/docs/in_application_api.html
    """
    def __init__(self, dll: CDLL):
        api = c_void_p()
        success = dll.RENDERDOC_GetAPI(RENDERDOC_Version.eRENDERDOC_API_Version_1_6_0.value, byref(api))
        if success != 1:
            raise SystemError(f"Failed to get renderdoc API: {success}")
        addr = cast(api, POINTER(c_void_p)).contents.value
        size = api.__sizeof__()
        # pRENDERDOC_GetAPIVersion GetAPIVersion;
        self._GetAPIVersion = CFUNCTYPE(None, POINTER(c_int), POINTER(c_int), POINTER(c_int))(addr)
        addr += size

        # pRENDERDOC_SetCaptureOptionU32 SetCaptureOptionU32;
        self._SetCaptureOptionU32 = CFUNCTYPE(c_int, c_int, c_uint32)(addr)
        addr += size
        # pRENDERDOC_SetCaptureOptionF32 SetCaptureOptionF32;
        self._SetCaptureOptionF32 = CFUNCTYPE(c_int, c_int, c_float)(addr)
        addr += size

        # pRENDERDOC_GetCaptureOptionU32 GetCaptureOptionU32;
        self._GetCaptureOptionU32 = CFUNCTYPE(c_uint32, c_int)(addr)
        addr += size
        # pRENDERDOC_GetCaptureOptionF32 GetCaptureOptionF32;
        self._GetCaptureOptionU32 = CFUNCTYPE(c_float, c_int)(addr)
        addr += size

        # pRENDERDOC_SetFocusToggleKeys SetFocusToggleKeys;
        self._SetFocusToggleKeys = CFUNCTYPE(None, POINTER(c_int), c_int)(addr)
        addr += size
        # pRENDERDOC_SetCaptureKeys SetCaptureKeys;
        self._SetCaptureKeys = CFUNCTYPE(None, POINTER(c_int), c_int)(addr)
        addr += size

        # pRENDERDOC_GetOverlayBits GetOverlayBits;
        self._GetOverlayBits = CFUNCTYPE(c_uint32)(addr)
        addr += size
        # pRENDERDOC_MaskOverlayBits MaskOverlayBits;
        self._MaskOverlayBits = CFUNCTYPE(None, c_uint32, c_uint32)(addr)
        addr += size

        # pRENDERDOC_RemoveHooks RemoveHooks;
        self._RemoveHooks = CFUNCTYPE(None)(addr)
        addr += size
        # pRENDERDOC_UnloadCrashHandler UnloadCrashHandler;
        self._UnloadCrashHandler = CFUNCTYPE(None)(addr)
        addr += size

        # pRENDERDOC_SetCaptureFilePathTemplate SetCaptureFilePathTemplate;
        self._SetCaptureFilePathTemplate = CFUNCTYPE(None, c_char_p)(addr)
        addr += size
        # pRENDERDOC_GetCaptureFilePathTemplate GetCaptureFilePathTemplate;
        self._GetCaptureFilePathTemplate = CFUNCTYPE(c_char_p)(addr)
        addr += size

        # pRENDERDOC_GetNumCaptures GetNumCaptures;
        self._GetNumCaptures = CFUNCTYPE(c_uint32)(addr)
        addr += size
        # pRENDERDOC_GetCapture GetCapture;
        self._GetCapture = CFUNCTYPE(c_uint32, c_uint32, c_char_p, POINTER(c_uint32), POINTER(c_uint64))(addr)
        addr += size

        # pRENDERDOC_TriggerCapture TriggerCapture;
        self._TriggerCapture = CFUNCTYPE(None)(addr)
        addr += size

        # pRENDERDOC_IsTargetControlConnected IsTargetControlConnected;
        self._IsTargetControlConnected = CFUNCTYPE(c_uint32)(addr)
        addr += size
        # pRENDERDOC_LaunchReplayUI LaunchReplayUI;
        self._LaunchReplayUI = CFUNCTYPE(c_uint32, c_uint32, c_char_p)(addr)
        addr += size

        # pRENDERDOC_SetActiveWindow SetActiveWindow;
        self._SetActiveWindow = CFUNCTYPE(None, c_void_p, c_void_p)(addr)
        addr += size

        # pRENDERDOC_StartFrameCapture StartFrameCapture;
        self._StartFrameCapture = CFUNCTYPE(None, c_void_p, c_void_p)(addr)
        addr += size
        # pRENDERDOC_IsFrameCapturing IsFrameCapturing;
        self._IsFrameCapturing = CFUNCTYPE(c_uint32)(addr)
        addr += size
        # pRENDERDOC_EndFrameCapture EndFrameCapture;
        self._EndFrameCapture = CFUNCTYPE(c_uint32, c_void_p, c_void_p)(addr)
        addr += size

        # pRENDERDOC_TriggerMultiFrameCapture TriggerMultiFrameCapture;
        self._TriggerMultiFrameCapture = CFUNCTYPE(None, c_uint32)(addr)
        addr += size

        # pRENDERDOC_SetCaptureFileComments SetCaptureFileComments;
        self._SetCaptureFileComments = CFUNCTYPE(None, c_char_p, c_char_p)(addr)
        addr += size

        # pRENDERDOC_DiscardFrameCapture DiscardFrameCapture;
        self._DiscardFrameCapture = CFUNCTYPE(c_uint32, c_void_p, c_void_p)(addr)
        addr += size

        # pRENDERDOC_ShowReplayUI ShowReplayUI;
        self._ShowReplayUI = CFUNCTYPE(c_uint32)(addr)
        addr += size

        # pRENDERDOC_SetCaptureTitle SetCaptureTitle;
        self._SetCaptureTitle = CFUNCTYPE(None, c_char_p)(addr)
        addr += size

    def get_api_version(self) -> (int, int, int):
        """
        RenderDoc can return a higher version than requested if it's backwards compatible,
        this function returns the actual version returned.
        :return: (major, minor, patch)
        """
        major, minor, patch = c_int(0), c_int(0), c_int(0)
        self._GetAPIVersion(byref(major), byref(minor), byref(patch))
        return major.value, minor.value, patch.value

    def set_capture_option_u32(self, option: RENDERDOC_CaptureOption, val: int) -> bool:
        """
        Sets an option that controls how RenderDoc behaves on capture.

        :param option: the option to set
        :param val: the value to set, must be castable to a uint32
        :return: ``True`` if the option and value are valid
        """
        return self._SetCaptureOptionU32(option.value, c_uint32(val)) == 1

    def set_capture_option_f32(self, option: RENDERDOC_CaptureOption, val: float) -> bool:
        """
        Sets an option that controls how RenderDoc behaves on capture.

        :param option: the option to set
        :param val: the value to set, must be castable to a float
        :return: ``True`` if the option and value are valid
        """
        return self._SetCaptureOptionU32(option.value, c_float(val)) == 1
