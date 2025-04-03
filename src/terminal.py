# Terminal
# Author: Daniel Ervilha
# Type: lib
import os

if os.name == 'nt':
    from i_terminal_win32 import read_input
   
# Public methods
def clear_screen():
    print("\033[2J\033[H", end='')

def clear_background():
    ...

def clear_foreground():
    ...

def cout(x: int, y: int, chars: str):
    print(chars, end='')
