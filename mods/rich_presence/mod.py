"""This module starts the Rich Presence Handler."""
import subprocess
import sys
import os

# Convert all relative paths to absolute paths at script start
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PRESENCE_EXE = os.path.join(SCRIPT_DIR, "presence.exe")

print("Starting Rich Presence Handler...")
subprocess.Popen(
    [PRESENCE_EXE],
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
sys.exit(0)
