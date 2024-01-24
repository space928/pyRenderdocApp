#  Copyright (c) 2019-2024 Thomas Mathieson.
#  Distributed under the terms of the MIT license.

import codecs
from ctypes import *
from datetime import datetime
from typing import Optional, List, Tuple
import sys
if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

from .renderdoc_enums import *

RenderDocDevicePointer: TypeAlias = c_void_p
"""
A device pointer is a pointer to the API's root handle.

This would be an ``ID3D11Device``, ``HGLRC``/``GLXContext``, ``ID3D12Device``, etc...
"""
RenderDocWindowHandle: TypeAlias = c_void_p
"""
A window handle is the OS's native window handle

This would be an ``HWND``, ``GLXDrawable``, etc
"""


class RENDERDOC_API_1_6_0:
    """
    RenderDoc API v1.6.0 wrapper, method names match those in renderdoc_app.h, with the caveat that they have been
    transformed to snake case (ie: ``GetAPIVersion()`` --> ``get_api_version()``). Documentation available at:
    https://renderdoc.org/docs/in_application_api.html
    """

    def __init__(self, dll: CDLL):
        api = c_void_p()
        success = dll.RENDERDOC_GetAPI(RENDERDOC_Version.eRENDERDOC_API_Version_1_6_0.value, byref(api))
        if success != 1:
            raise SystemError(f"Failed to get renderdoc API: {success}")
        addr = api  # cast(api, POINTER(c_void_p)).contents.value

        def next_addr():
            nonlocal addr
            ret = cast(addr, POINTER(c_void_p)).contents.value
            addr.value += size
            return ret

        size = sizeof(c_void_p)
        # pRENDERDOC_GetAPIVersion GetAPIVersion;
        self._GetAPIVersion = CFUNCTYPE(None, POINTER(c_int), POINTER(c_int), POINTER(c_int))(next_addr())

        # pRENDERDOC_SetCaptureOptionU32 SetCaptureOptionU32;
        self._SetCaptureOptionU32 = CFUNCTYPE(c_int, c_int, c_uint32)(next_addr())
        # pRENDERDOC_SetCaptureOptionF32 SetCaptureOptionF32;
        self._SetCaptureOptionF32 = CFUNCTYPE(c_int, c_int, c_float)(next_addr())

        # pRENDERDOC_GetCaptureOptionU32 GetCaptureOptionU32;
        self._GetCaptureOptionU32 = CFUNCTYPE(c_uint32, c_int)(next_addr())
        # pRENDERDOC_GetCaptureOptionF32 GetCaptureOptionF32;
        self._GetCaptureOptionF32 = CFUNCTYPE(c_float, c_int)(next_addr())

        # pRENDERDOC_SetFocusToggleKeys SetFocusToggleKeys;
        self._SetFocusToggleKeys = CFUNCTYPE(None, POINTER(c_int), c_int)(next_addr())
        # pRENDERDOC_SetCaptureKeys SetCaptureKeys;
        self._SetCaptureKeys = CFUNCTYPE(None, POINTER(c_int), c_int)(next_addr())

        # pRENDERDOC_GetOverlayBits GetOverlayBits;
        self._GetOverlayBits = CFUNCTYPE(c_uint32)(next_addr())
        # pRENDERDOC_MaskOverlayBits MaskOverlayBits;
        self._MaskOverlayBits = CFUNCTYPE(None, c_uint32, c_uint32)(next_addr())

        # pRENDERDOC_RemoveHooks RemoveHooks;
        self._RemoveHooks = CFUNCTYPE(None)(next_addr())
        # pRENDERDOC_UnloadCrashHandler UnloadCrashHandler;
        self._UnloadCrashHandler = CFUNCTYPE(None)(next_addr())

        # pRENDERDOC_SetCaptureFilePathTemplate SetCaptureFilePathTemplate;
        self._SetCaptureFilePathTemplate = CFUNCTYPE(None, c_char_p)(next_addr())
        # pRENDERDOC_GetCaptureFilePathTemplate GetCaptureFilePathTemplate;
        self._GetCaptureFilePathTemplate = CFUNCTYPE(c_char_p)(next_addr())

        # pRENDERDOC_GetNumCaptures GetNumCaptures;
        self._GetNumCaptures = CFUNCTYPE(c_uint32)(next_addr())
        # pRENDERDOC_GetCapture GetCapture;
        self._GetCapture = CFUNCTYPE(c_uint32, c_uint32, c_char_p, POINTER(c_uint32), POINTER(c_uint64))(next_addr())

        # pRENDERDOC_TriggerCapture TriggerCapture;
        self._TriggerCapture = CFUNCTYPE(None)(next_addr())

        # pRENDERDOC_IsTargetControlConnected IsTargetControlConnected;
        self._IsTargetControlConnected = CFUNCTYPE(c_uint32)(next_addr())
        # pRENDERDOC_LaunchReplayUI LaunchReplayUI;
        self._LaunchReplayUI = CFUNCTYPE(c_uint32, c_uint32, c_char_p)(next_addr())

        # pRENDERDOC_SetActiveWindow SetActiveWindow;
        self._SetActiveWindow = CFUNCTYPE(None, c_void_p, c_void_p)(next_addr())

        # pRENDERDOC_StartFrameCapture StartFrameCapture;
        self._StartFrameCapture = CFUNCTYPE(None, c_void_p, c_void_p)(next_addr())
        # pRENDERDOC_IsFrameCapturing IsFrameCapturing;
        self._IsFrameCapturing = CFUNCTYPE(c_uint32)(next_addr())
        # pRENDERDOC_EndFrameCapture EndFrameCapture;
        self._EndFrameCapture = CFUNCTYPE(c_uint32, c_void_p, c_void_p)(next_addr())

        # pRENDERDOC_TriggerMultiFrameCapture TriggerMultiFrameCapture;
        self._TriggerMultiFrameCapture = CFUNCTYPE(None, c_uint32)(next_addr())

        # pRENDERDOC_SetCaptureFileComments SetCaptureFileComments;
        self._SetCaptureFileComments = CFUNCTYPE(None, c_char_p, c_char_p)(next_addr())

        # pRENDERDOC_DiscardFrameCapture DiscardFrameCapture;
        self._DiscardFrameCapture = CFUNCTYPE(c_uint32, c_void_p, c_void_p)(next_addr())

        # pRENDERDOC_ShowReplayUI ShowReplayUI;
        self._ShowReplayUI = CFUNCTYPE(c_uint32)(next_addr())

        # pRENDERDOC_SetCaptureTitle SetCaptureTitle;
        self._SetCaptureTitle = CFUNCTYPE(None, c_char_p)(next_addr())

    @staticmethod
    def _encode_str(s: Optional[str]) -> c_char_p:
        """
        Converts a string to a c_char_p.

        :param s:
        :return:
        """
        return c_char_p(b"") if s is None else c_char_p(codecs.encode(s, encoding="utf-8"))

    def get_api_version(self) -> Tuple[int, int, int]:
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

    def get_capture_option_u32(self, option: RENDERDOC_CaptureOption) -> int:
        """
        Gets an option that controls how RenderDoc behaves on capture.

        :param option: the option to get
        :return: ``0xffffffff`` if the option is invalid
        """
        return self._GetCaptureOptionU32(option.value)

    def get_capture_option_f32(self, option: RENDERDOC_CaptureOption) -> float:
        """
        Gets an option that controls how RenderDoc behaves on capture.

        :param option: the option to get
        :return: ``-FLT_MAX`` if the option is invalid
        """
        return self._GetCaptureOptionF32(option.value)

    def set_focus_toggle_keys(self, keys: Optional[List[RENDERDOC_InputButton]]) -> None:
        """
        Sets which key or keys can be used to toggle focus between multiple windows

        If keys is ``None`` or len is 0, toggle keys will be disabled
        :param keys: list of keys to use.
        """
        keys_arr = c_void_p(0) if keys is None else (c_int * len(keys))(*(k.value for k in keys))
        n = 0 if keys is None else len(keys)
        self._SetFocusToggleKeys(keys_arr, n)

    def set_capture_keys(self, keys: Optional[List[RENDERDOC_InputButton]]) -> None:
        """
        Sets which key or keys can be used to capture the next frame

        If keys is ``None`` or len is 0, capture keys will be disabled
        :param keys: list of keys to use.
        """
        keys_arr = c_void_p(0) if keys is None else (c_int * len(keys))(*(k.value for k in keys))
        n = 0 if keys is None else len(keys)
        self._SetCaptureKeys(keys_arr, n)

    def get_overlay_bits(self) -> RENDERDOC_OverlayBits:
        """
        Gets the overlay bits that have been set.

        :return: the overlay bits that have been set.
        """
        return RENDERDOC_OverlayBits(self._GetOverlayBits())

    def mask_overlay_bits(self, _and: RENDERDOC_OverlayBits, _or: RENDERDOC_OverlayBits) -> None:
        """
        Sets the overlay bits with an and & or mask

        :param _and: bits to and with the current mask.
        :param _or: bits to or with the current mask.
        """
        # noinspection PyTypeChecker
        self._MaskOverlayBits(c_uint32(_and.value), c_uint32(_or.value))

    def remove_hooks(self) -> None:
        """
        This function will attempt to remove RenderDoc's hooks in the application.

        Note: that this can only work correctly if done immediately after
        the module is loaded, before any API work happens. RenderDoc will remove its
        injected hooks and shut down. Behaviour is undefined if this is called
        after any API functions have been called, and there is still no guarantee of
        success.
        """
        self._RemoveHooks()

    def unload_crash_handler(self) -> None:
        """
        This function will unload RenderDoc's crash handler.

        If you use your own crash handler and don't want RenderDoc's handler to
        intercede, you can call this function to unload it and any unhandled
        exceptions will pass to the next handler.
        """
        self._UnloadCrashHandler()

    def set_capture_file_path_template(self, path_template: Optional[str]) -> None:
        """
        Sets the capture file path template

        ``path_template`` is a UTF-8 string that gives a template for how captures will be named
        and where they will be saved.

        Any extension is stripped off the path, and captures are saved in the directory
        specified, and named with the filename and the frame number appended. If the
        directory does not exist it will be created, including any parent directories.

        If ``path_template`` is ``None``, the template will remain unchanged

        *Example:*
            ``SetCaptureFilePathTemplate("my_captures/example");``

            ``Capture #1 -> my_captures/example_frame123.rdc``
            ``Capture #2 -> my_captures/example_frame456.rdc``

        :param path_template: a string that gives a template for how captures will be
                              named and where they will be saved.
        """
        self._SetCaptureFilePathTemplate(self._encode_str(path_template))

    def get_capture_file_path_template(self) -> str:
        """
        Gets the current capture path template.

        :return: the current capture path template, see SetCaptureFileTemplate above, as a UTF-8 string.
        """
        path: c_char_p = self._GetCaptureFilePathTemplate()
        return "" if path is None else codecs.decode(path, encoding="utf-8")

    def get_num_captures(self) -> int:
        """
        Gets the number of captures that have been made.
        :return: the number of captures that have been made.
        """
        return self._GetNumCaptures()

    def get_capture(self, idx: int) -> Tuple[bool, str, int, datetime]:
        """
        This function returns the details of a capture, by index. New captures are added
        to the end of the list.

        The function will return ``True`` if the capture index is valid, or ``False`` if the index is invalid

        Note: when captures are deleted in the UI they will remain in this list, so the
        capture path may not exist anymore.

        :param idx: the index of the capture to retrieve
        :return: (whether the capture index is valid,
                  the absolute path to the capture file,
                  length in bytes of the filename string,
                  the time of the capture).
        """
        filename = c_char_p(bytes(512))
        pathlength = c_uint32(0)
        timestamp = c_uint64(0)
        success = self._GetCapture(c_uint32(idx), filename, byref(pathlength), byref(timestamp))
        filename_bytes = filename.value
        return (success == 1,
                "" if filename_bytes is None else codecs.decode(filename_bytes, encoding="utf-8"),
                pathlength.value,
                datetime.fromtimestamp(timestamp.value))

    def set_capture_file_comments(self, file_path: Optional[str], comments: str) -> None:
        """
        Sets the comments associated with a capture file. These comments are displayed in the
        UI program when opening.

        ``file_path`` should be a path to the capture file to add comments to. If set to ``None`` or ""
        the most recent capture file created made will be used instead.
        comments should be a NULL-terminated UTF-8 string to add as comments.

        Any existing comments will be overwritten.

        :param file_path: the path to the capture file to add comments to.
        :param comments: the comments to add to the capture file.
        """
        self._SetCaptureFileComments(self._encode_str(file_path), self._encode_str(comments))

    def is_target_control_connected(self) -> bool:
        """
        Returns ``True`` if the RenderDoc UI is connected to this application.

        :return: ``True`` if the RenderDoc UI is connected to this application.
        """
        return self._IsTargetControlConnected() == 1

    def launch_replay_ui(self, connect_target_control: bool, cmd_line: Optional[str]) -> int:
        """
        This function will launch the Replay UI associated with the RenderDoc library injected
        into the running application.

        :param connect_target_control: if ``True``, the Replay UI will be launched with a command
                                       line parameter to connect to this application.
        :param cmd_line: the rest of the command line, as a UTF-8 string. E.g. a captures to open
                         if cmdline is ``None``, the command line will be empty.
        :return: the PID of the replay UI if successful, 0 if not successful.
        """
        return self._LaunchReplayUI(c_uint32(1 if connect_target_control else 0),
                                    c_char_p(None if cmd_line is None else codecs.encode(cmd_line, encoding="utf-8")))

    def show_replay_ui(self) -> bool:
        """
        Requests that the replay UI show itself (if hidden or not the current top window). This can be
        used in conjunction with IsTargetControlConnected and LaunchReplayUI to intelligently handle
        showing the UI after making a capture.

        :return: ``True`` if the request was successfully passed on, though it's not guaranteed that
                 the UI will be on top in all cases depending on OS rules. It will return ``False``
                 if there is no current control connection to make such a request, or if there was
                 another error.
        """
        return self._ShowReplayUI() == 1

    def set_active_window(self, device: RenderDocDevicePointer, wnd_handle: RenderDocWindowHandle) -> None:
        """
        This sets the RenderDoc in-app overlay in the API/window pair as 'active' and it will
        respond to keypresses. Neither parameter can be ``None``.

        :param device: the pointer to the graphics API's device (This would be an ``ID3D11Device``,
                       ``HGLRC``/``GLXContext``, ``ID3D12Device``, etc...).
        :param wnd_handle: the handle to the OS window (This would be an ``HWND``, ``GLXDrawable``, etc...).
        """
        self._SetActiveWindow(device, wnd_handle)

    def trigger_capture(self) -> None:
        """
        Capture the next frame on whichever window and API is currently considered active.
        """
        self._TriggerCapture()

    def trigger_multi_frame_capture(self, num_frames: int) -> None:
        """
        Capture the next N frames on whichever window and API is currently considered active.

        :param num_frames: how many frames to capture.
        """
        self._TriggerMultiFrameCapture(c_uint32(num_frames))

    def start_frame_capture(self, device: Optional[RenderDocDevicePointer],
                            wnd_handle: Optional[RenderDocWindowHandle]) -> None:
        """
        When choosing either a device pointer or a window handle to capture, you can pass ``None``.
        Passing ``None`` specifies a 'wildcard' match against anything. This allows you to specify
        any API rendering to a specific window, or a specific API instance rendering to any window,
        or in the simplest case of one window and one API, you can just pass NULL for both.

        In either case, if there are two or more possible matching (device,window) pairs it
        is undefined which one will be captured.

        Note: for headless rendering you can pass ``None`` for the window handle and either specify
        a device pointer or leave it ``None`` as above.

        Immediately starts capturing API calls on the specified device pointer and window handle.

        If there is no matching thing to capture (e.g. no supported API has been initialised),
        this will do nothing.

        The results are undefined (including crashes) if two captures are started overlapping,
        even on separate devices and/or windows.

        :param device: the pointer to the graphics API's device (This would be an ``ID3D11Device``,
                       ``HGLRC``/``GLXContext``, ``ID3D12Device``, etc...).
        :param wnd_handle: the handle to the OS window (This would be an ``HWND``, ``GLXDrawable``, etc...).
        """
        if device is None:
            device = c_void_p(None)
        if wnd_handle is None:
            wnd_handle = c_void_p(None)
        self._StartFrameCapture(device, wnd_handle)

    def is_frame_capturing(self) -> bool:
        """
        Checks if a frame capture is currently ongoing anywhere.

        :return: ``True`` if a capture is ongoing, and ``False`` if there is no capture running.
        """
        return self._IsFrameCapturing() == 1

    def end_frame_capture(self, device: Optional[RenderDocDevicePointer],
                          wnd_handle: Optional[RenderDocWindowHandle]) -> bool:
        """
        Ends capturing immediately.

        :param device: the pointer to the graphics API's device (This would be an ``ID3D11Device``,
                       ``HGLRC``/``GLXContext``, ``ID3D12Device``, etc...).
        :param wnd_handle: the handle to the OS window (This would be an ``HWND``, ``GLXDrawable``, etc...).
        :return: ``True`` if the capture succeeded, and ``False`` if there was an error capturing.
        """
        if device is None:
            device = c_void_p(None)
        if wnd_handle is None:
            wnd_handle = c_void_p(None)
        return self._EndFrameCapture(device, wnd_handle) == 1

    def discard_frame_capture(self, device: Optional[RenderDocDevicePointer],
                              wnd_handle: Optional[RenderDocWindowHandle]) -> bool:
        """
        Ends capturing immediately and discard any data stored without saving to disk.

        :param device: the pointer to the graphics API's device (This would be an ``ID3D11Device``,
                       ``HGLRC``/``GLXContext``, ``ID3D12Device``, etc...).
        :param wnd_handle: the handle to the OS window (This would be an ``HWND``, ``GLXDrawable``, etc...).
        :return: ``True`` if the capture was discarded, and ``False`` if there was an error capturing or no capture was
                 in progress.
        """
        if device is None:
            device = c_void_p(None)
        if wnd_handle is None:
            wnd_handle = c_void_p(None)
        return self._DiscardFrameCapture(device, wnd_handle) == 1

    def set_capture_title(self, title: str) -> None:
        """
        Only valid to be called between a call to StartFrameCapture and EndFrameCapture. Gives a custom
        title to the capture produced which will be displayed in the UI.

        If multiple captures are ongoing, this title will be applied to the first capture to end after
        this call. The second capture to end will have no title, unless this function is called again.

        Calling this function has no effect if no capture is currently running, and if it is called
        multiple times only the last title will be used.

        :param title: the title to give the capture.
        """
        self._SetCaptureTitle(self._encode_str(title))
