#  Copyright (c) 2023 Thomas Mathieson.
#  Distributed under the terms of the MIT license.
# Ported from renderdoc_app.h, available under the MIT license Copyright (c) 2019-2023 Baldur Karlsson
# https://github.com/baldurk/renderdoc/blob/v1.x/renderdoc/api/app/renderdoc_app.h

from enum import Enum, Flag


class RENDERDOC_Version(Enum):
    eRENDERDOC_API_Version_1_0_0 = 10000
    eRENDERDOC_API_Version_1_0_1 = 10001
    eRENDERDOC_API_Version_1_0_2 = 10002
    eRENDERDOC_API_Version_1_1_0 = 10100
    eRENDERDOC_API_Version_1_1_1 = 10101
    eRENDERDOC_API_Version_1_1_2 = 10102
    eRENDERDOC_API_Version_1_2_0 = 10200
    eRENDERDOC_API_Version_1_3_0 = 10300
    eRENDERDOC_API_Version_1_4_0 = 10400
    eRENDERDOC_API_Version_1_4_1 = 10401
    eRENDERDOC_API_Version_1_4_2 = 10402
    eRENDERDOC_API_Version_1_5_0 = 10500
    eRENDERDOC_API_Version_1_6_0 = 10600


class RENDERDOC_CaptureOption(Enum):
    """
    RenderDoc capture options
    """
    eRENDERDOC_Option_AllowVSync = 0,
    """
    Allow the application to enable vsync

    Default - enabled

     - 1 - The application can enable or disable vsync at will
     - 0 - vsync is force disabled
    """

    eRENDERDOC_Option_AllowFullscreen = 1
    """
    Allow the application to enable fullscreen

    Default - enabled

     - 1 - The application can enable or disable fullscreen at will
     - 0 - fullscreen is force disabled
    """

    eRENDERDOC_Option_APIValidation = 2
    """
    Record API debugging events and messages

    Default - disabled

     - 1 - Enable built-in API debugging features and records the results into
       the capture, which is matched up with events on replay
     - 0 - no API debugging is forcibly enabled
    """
    eRENDERDOC_Option_DebugDeviceMode = 2
    """
    Record API debugging events and messages

    Default - disabled

     - 1 - Enable built-in API debugging features and records the results into
       the capture, which is matched up with events on replay
     - 0 - no API debugging is forcibly enabled
    """

    eRENDERDOC_Option_CaptureCallstacks = 3
    """
    Capture CPU callstacks for API events

    Default - disabled

     - 1 - Enables capturing of callstacks
     - 0 - no callstacks are captured
    """

    eRENDERDOC_Option_CaptureCallstacksOnlyDraws = 4
    """
    When capturing CPU callstacks, only capture them from actions.
    This option does nothing without the above option being enabled

    Default - disabled

     - 1 - Only captures callstacks for actions.
       Ignored if CaptureCallstacks is disabled
     - 0 - Callstacks, if enabled, are captured for every event.
    """
    eRENDERDOC_Option_CaptureCallstacksOnlyActions = 4
    """
    When capturing CPU callstacks, only capture them from actions.
    This option does nothing without the above option being enabled

    Default - disabled

     - 1 - Only captures callstacks for actions.
       Ignored if CaptureCallstacks is disabled
     - 0 - Callstacks, if enabled, are captured for every event.
    """

    eRENDERDOC_Option_DelayForDebugger = 5
    """
    Specify a delay in seconds to wait for a debugger to attach, after
    creating or injecting into a process, before continuing to allow it to run.

    0 indicates no delay, and the process will run immediately after injection

    Default - 0 seconds
    """

    eRENDERDOC_Option_VerifyBufferAccess = 6
    """
    Verify buffer access. This includes checking the memory returned by a Map() call to
    detect any out-of-bounds modification, as well as initialising buffers with undefined contents
    to a marker value to catch use of uninitialised memory.

    NOTE: This option is only valid for OpenGL and D3D11. Explicit APIs such as D3D12 and Vulkan do
    not do the same kind of interception & checking and undefined contents are really undefined.

    Default - disabled

     - 1 - Verify buffer access
     - 0 - No verification is performed, and overwriting bounds may cause crashes or corruption in RenderDoc.
    """

    eRENDERDOC_Option_HookIntoChildren = 7
    """
    The old name for eRENDERDOC_Option_VerifyBufferAccess was eRENDERDOC_Option_VerifyMapWrites.
    This option now controls the filling of uninitialised buffers with 0xdddddddd which was
    previously always enabled
    NDERDOC_Option_VerifyMapWrites = eRENDERDOC_Option_VerifyBufferAccess,

    Hooks any system API calls that create child processes, and injects
    RenderDoc into them recursively with the same options.

    Default - disabled

     - 1 - Hooks into spawned child processes
     - 0 - Child processes are not hooked by RenderDoc
    """

    eRENDERDOC_Option_RefAllResources = 8
    """
    By default RenderDoc only includes resources in the final capture necessary
    for that frame, this allows you to override that behaviour.

    Default - disabled

     - 1 - all live resources at the time of capture are included in the capture
       and available for inspection
     - 0 - only the resources referenced by the captured frame are included
    """

    eRENDERDOC_Option_SaveAllInitials = 9
    """
    **NOTE**: As of RenderDoc v1.1 this option has been deprecated. Setting or
    getting it will be ignored, to allow compatibility with older versions.
    In v1.1 the option acts as if it's always enabled.

    By default RenderDoc skips saving initial states for resources where the
    previous contents don't appear to be used, assuming that writes before
    reads indicate previous contents aren't used.

    Default - disabled

     - 1 - initial contents at the start of each captured frame are saved, even if
       they are later overwritten or cleared before being used.
     - 0 - unless a read is detected, initial contents will not be saved and will
       appear as black or empty data.
    """

    eRENDERDOC_Option_CaptureAllCmdLists = 10
    """
    In APIs that allow for the recording of command lists to be replayed later,
    RenderDoc may choose to not capture command lists before a frame capture is
    triggered, to reduce overheads. This means any command lists recorded once
    and replayed many times will not be available and may cause a failure to
    capture.

    NOTE: This is only true for APIs where multithreading is difficult or
    discouraged. Newer APIs like Vulkan and D3D12 will ignore this option
    and always capture all command lists since the API is heavily oriented
    around it and the overheads have been reduced by API design.

    - 1 - All command lists are captured from the start of the application
    - 0 - Command lists are only captured if their recording begins during
      the period when a frame capture is in progress.
    """

    eRENDERDOC_Option_DebugOutputMute = 11
    """
    Mute API debugging output when the API validation mode option is enabled

    Default - enabled

    1 - Mute any API debug messages from being displayed or passed through
    0 - API debugging is displayed as normal
    """

    eRENDERDOC_Option_AllowUnsupportedVendorExtensions = 12
    """
    Option to allow vendor extensions to be used even when they may be
    incompatible with RenderDoc and cause corrupted replays or crashes.

    Default - inactive

    No values are documented, this option should only be used when absolutely
    necessary as directed by a RenderDoc developer.
    """

    eRENDERDOC_Option_SoftMemoryLimit = 13
    """
    Define a soft memory limit which some APIs may aim to keep overhead under where
    possible. Anything above this limit will where possible be saved directly to disk during
    capture.
    This will cause increased disk space use (which may cause a capture to fail if disk space is
    exhausted) as well as slower capture times.

    Not all memory allocations may be deferred like this so it is not a guarantee of a memory
    limit.

    Units are in MBs, suggested values would range from 200MB to 1000MB.

    Default - 0 Megabytes
    """


class RENDERDOC_InputButton(Enum):
    # '0' - '9' matches ASCII values
    eRENDERDOC_Key_0 = 0x30
    eRENDERDOC_Key_1 = 0x31
    eRENDERDOC_Key_2 = 0x32
    eRENDERDOC_Key_3 = 0x33
    eRENDERDOC_Key_4 = 0x34
    eRENDERDOC_Key_5 = 0x35
    eRENDERDOC_Key_6 = 0x36
    eRENDERDOC_Key_7 = 0x37
    eRENDERDOC_Key_8 = 0x38
    eRENDERDOC_Key_9 = 0x39

    # 'A' - 'Z' matches ASCII values
    eRENDERDOC_Key_A = 0x41
    eRENDERDOC_Key_B = 0x42
    eRENDERDOC_Key_C = 0x43
    eRENDERDOC_Key_D = 0x44
    eRENDERDOC_Key_E = 0x45
    eRENDERDOC_Key_F = 0x46
    eRENDERDOC_Key_G = 0x47
    eRENDERDOC_Key_H = 0x48
    eRENDERDOC_Key_I = 0x49
    eRENDERDOC_Key_J = 0x4A
    eRENDERDOC_Key_K = 0x4B
    eRENDERDOC_Key_L = 0x4C
    eRENDERDOC_Key_M = 0x4D
    eRENDERDOC_Key_N = 0x4E
    eRENDERDOC_Key_O = 0x4F
    eRENDERDOC_Key_P = 0x50
    eRENDERDOC_Key_Q = 0x51
    eRENDERDOC_Key_R = 0x52
    eRENDERDOC_Key_S = 0x53
    eRENDERDOC_Key_T = 0x54
    eRENDERDOC_Key_U = 0x55
    eRENDERDOC_Key_V = 0x56
    eRENDERDOC_Key_W = 0x57
    eRENDERDOC_Key_X = 0x58
    eRENDERDOC_Key_Y = 0x59
    eRENDERDOC_Key_Z = 0x5A

    # leave the rest of the ASCII range free
    # in case we want to use it later
    eRENDERDOC_Key_NonPrintable = 0x100

    eRENDERDOC_Key_Divide = 0x101
    eRENDERDOC_Key_Multiply = 0x102
    eRENDERDOC_Key_Subtract = 0x103
    eRENDERDOC_Key_Plus = 0x104

    eRENDERDOC_Key_F1 = 0x105
    eRENDERDOC_Key_F2 = 0x106
    eRENDERDOC_Key_F3 = 0x107
    eRENDERDOC_Key_F4 = 0x108
    eRENDERDOC_Key_F5 = 0x109
    eRENDERDOC_Key_F6 = 0x10A
    eRENDERDOC_Key_F7 = 0x10B
    eRENDERDOC_Key_F8 = 0x10C
    eRENDERDOC_Key_F9 = 0x10D
    eRENDERDOC_Key_F10 = 0x10E
    eRENDERDOC_Key_F11 = 0x10F
    eRENDERDOC_Key_F12 = 0x110

    eRENDERDOC_Key_Home = 0x111
    eRENDERDOC_Key_End = 0x112
    eRENDERDOC_Key_Insert = 0x113
    eRENDERDOC_Key_Delete = 0x114
    eRENDERDOC_Key_PageUp = 0x115
    eRENDERDOC_Key_PageDn = 0x116

    eRENDERDOC_Key_Backspace = 0x117
    eRENDERDOC_Key_Tab = 0x118
    eRENDERDOC_Key_PrtScrn = 0x119
    eRENDERDOC_Key_Pause = 0x11A

    eRENDERDOC_Key_Max = 0x11B


class RENDERDOC_OverlayBits(Flag):
    # This single bit controls whether the overlay is enabled or disabled globally
    eRENDERDOC_Overlay_Enabled = 0x1

    # Show the average framerate over several seconds as well as min/max
    eRENDERDOC_Overlay_FrameRate = 0x2

    # Show the current frame number
    eRENDERDOC_Overlay_FrameNumber = 0x4

    # Show a list of recent captures, and how many captures have been made
    eRENDERDOC_Overlay_CaptureList = 0x8

    # Default values for the overlay mask
    eRENDERDOC_Overlay_Default = (eRENDERDOC_Overlay_Enabled | eRENDERDOC_Overlay_FrameRate |
                                  eRENDERDOC_Overlay_FrameNumber | eRENDERDOC_Overlay_CaptureList)

    # Enable all bits
    eRENDERDOC_Overlay_All = 0xffffffff

    # Disable all bits
    eRENDERDOC_Overlay_None = 0
