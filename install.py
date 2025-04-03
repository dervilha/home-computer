# Install
# Author: Daniel Ervilha
# Type: routine

# References
# - pyinstaller documentation: https://pyinstaller.org/en/stable/man/pyinstaller.html

# Known issues
# - not tested outside win32 environment

import os
import subprocess

ICON = 'icon.ico'
NAME = 'HomeComputer'

WIN32 = os.name == 'nt'
PIP = "pip" if WIN32 else "pip3"

if subprocess.run('pyinstaller --version', capture_output=True).check_returncode():
    print(f'{PIP} install pyinstaller')

# Run pyinstaller (create executable)
subprocess.run([
    'pyinstaller',
    '--onefile',
    '--clean',
    '--icon', ICON,
    '--name', NAME,
    '--distpath', '.',
    '--paths=./src',
    'src/main.py'
])
