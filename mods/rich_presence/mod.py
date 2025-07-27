"""This module starts the Rich Presence Handler."""
import subprocess
import sys

print("Starting Rich Presence Handler...")
subprocess.Popen(
    ["mods\\rich_presence\\presence.exe"],
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
sys.exit(0)
