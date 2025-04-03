import os
import subprocess

# Start the process in the background
process = subprocess.Popen(
    ["your_command", "arg1", "arg2"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True  # or use encoding='utf-8'
)

# ... do other things while the process runs in the background ...

# To get the output later
stdout, stderr = process.communicate()

print("STDOUT:", stdout)
print("STDERR:", stderr)

for line in process.stdout:
    print(line.strip())


# new window

import subprocess
import sys

subprocess.Popen(
    [sys.executable, "-c", "print('Hello from new window!'); input('Press Enter to exit...')"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)
subprocess.Popen(
    ["ping", "google.com"],
    creationflags=subprocess.CREATE_NEW_CONSOLE
)


if os.name == 'nt': # Win32
    def run(process: str | list[str]) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(process, shell=True, capture_output=True)
    
    def new(process: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run('start ' + process, shell=True)

    def run_background(process: str) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run('start /b ' + process, shell=True, capture_output=True)


else:
    ...


