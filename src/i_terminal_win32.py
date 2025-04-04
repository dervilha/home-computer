# Windows Terminal Input
# Author: Daniel Ervilha
# Type: lib

# Known issues
# - Mouse Events missing button release
# - missing some event types

import ctypes
import ctypes.wintypes as wintypes

# Constants from Windows API
STD_INPUT_HANDLE = -10
ENABLE_MOUSE_INPUT = 0x0010
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_WINDOW_INPUT = 0x0008

KEY_EVENT = 0x0001
MOUSE_EVENT = 0x0002

FROM_LEFT_1ST_BUTTON_PRESSED = 0x0001
RIGHTMOST_BUTTON_PRESSED = 0x0002
MOUSE_MOVED = 0x0001
MOUSE_WHEELED = 0x0004

# Structs from Windows API
class COORD(ctypes.Structure):
    _fields_ = [("X", wintypes.SHORT), ("Y", wintypes.SHORT)]

class KEY_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ("bKeyDown", wintypes.BOOL),
        ("wRepeatCount", wintypes.WORD),
        ("wVirtualKeyCode", wintypes.WORD),
        ("wVirtualScanCode", wintypes.WORD),
        ("uChar", wintypes.WCHAR),
        ("dwControlKeyState", wintypes.DWORD),
    ]

class MOUSE_EVENT_RECORD(ctypes.Structure):
    _fields_ = [
        ("dwMousePosition", COORD),
        ("dwButtonState", wintypes.DWORD),
        ("dwControlKeyState", wintypes.DWORD),
        ("dwEventFlags", wintypes.DWORD),
    ]

class EVENT_UNION(ctypes.Union):
    _fields_ = [
        ("KeyEvent", KEY_EVENT_RECORD),
        ("MouseEvent", MOUSE_EVENT_RECORD),
    ]

class INPUT_RECORD(ctypes.Structure):
    _fields_ = [
        ("EventType", wintypes.WORD),
        ("Event", EVENT_UNION),
    ]

kernel32 = ctypes.windll.kernel32
handle = kernel32.GetStdHandle(STD_INPUT_HANDLE)

kernel32.SetConsoleMode(
    handle,
    ENABLE_EXTENDED_FLAGS | ENABLE_MOUSE_INPUT | ENABLE_WINDOW_INPUT
)

_forced_event_stack = []
def force_input(event):
    _forced_event_stack.append(event)

def read_input():
    if _forced_event_stack:
        return _forced_event_stack.pop()

    record = INPUT_RECORD()
    count = wintypes.DWORD()

    # success = kernel32.ReadConsoleInputW(handle, ctypes.byref(record), 1, ctypes.byref(count))
    success = kernel32.PeekConsoleInputW(handle, ctypes.byref(record), 1, ctypes.byref(count))
    if not success or count.value == 0:
        return None

    kernel32.ReadConsoleInputW(handle, ctypes.byref(record), 1, ctypes.byref(count))

    if record.EventType == KEY_EVENT:
        key = record.Event.KeyEvent

        return {
            'type': KEY_EVENT,
            'key': ord(key.uChar),
            'press': key.bKeyDown,
            'keycode': key.wVirtualKeyCode,
            'scancode': key.wVirtualScanCode
        }

    if record.EventType == MOUSE_EVENT:
        mouse = record.Event.MouseEvent
        x, y = mouse.dwMousePosition.X, mouse.dwMousePosition.Y
        state = mouse.dwButtonState
        event_flags = mouse.dwEventFlags

        if event_flags == 0:
            if state & FROM_LEFT_1ST_BUTTON_PRESSED:
                return {'type': 'mouse', 'event': 'press', 'button': 'left', 'x': x, 'y': y, 'state': state}
            elif state & RIGHTMOST_BUTTON_PRESSED:
                return {'type': 'mouse', 'event': 'press', 'button': 'right', 'x': x, 'y': y, 'state': state}
        elif event_flags == MOUSE_MOVED:
            return {'type': 'mouse', 'event': 'move', 'x': x, 'y': y, 'state': state}
        elif event_flags == MOUSE_WHEELED:
            return {'type': 'mouse', 'event': 'wheel', 'x': x, 'y': y, 'state':state}
     

def hide_cursor():
    # Get the handle to the console output
    stdout_handle = ctypes.windll.kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11

    # Define the CONSOLE_CURSOR_INFO structure
    class CONSOLE_CURSOR_INFO(ctypes.Structure):
        _fields_ = [("dwSize", ctypes.c_int),
                    ("bVisible", ctypes.c_bool)]

    # Create an instance and set cursor visibility to False
    cursor_info = CONSOLE_CURSOR_INFO()
    ctypes.windll.kernel32.GetConsoleCursorInfo(stdout_handle, ctypes.byref(cursor_info))
    cursor_info.bVisible = False
    ctypes.windll.kernel32.SetConsoleCursorInfo(stdout_handle, ctypes.byref(cursor_info))