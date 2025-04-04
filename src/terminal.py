# Terminal
# Author: Daniel Ervilha
# Type: lib
import os

EVENT_KEYBOARD = 1
EVENT_MOUSE = 2
EVENT_RESIZE = 3

if os.name == 'nt':
    from i_terminal_win32 import read_input, force_input, hide_cursor
   
def size():
    ts = os.get_terminal_size()
    return ts.columns, ts.lines

def clear_screen():
    print("\033[2J\033[H", end='')
