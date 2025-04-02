# Name: Build
# Author: Daniel Ervilha
# Type: ROUTINE

# References
# - pyinstaller documentation: https://pyinstaller.org/en/stable/man/pyinstaller.html

import os
import subprocess

ICON = 'icon.ico'
NAME = 'HomeComputer'

WIN32 = os.name == 'nt'
PIP = "pip" if WIN32 else "pip3"

if subprocess.run('pyinstaller --version', capture_output=True).check_returncode():
    print(f'{PIP} install pyinstaller')

subprocess.run([
    'pyinstaller',
    '--onefile',
    '--clean',
    '--icon', ICON,
    '--name', NAME,
    # '--specpath', 'build',
    'core/main.py'
])
