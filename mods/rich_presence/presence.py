"""OpenADB Shell Rich Presence Module"""
from time import time, sleep
import os
import sys
import datetime
from threading import Thread
from pypresence import Presence


def update_vars():
    """Update variables from files"""
    global enabled_rich_presence, devices, exiting
    try:
        while True:
            with open(os.path.join("mods", "rich_presence",
                                   "enabled.dat"), "r", encoding="utf-8"
                      ) as datafile:
                enabled_rich_presence = datafile.read().strip() == "1"
                datafile.close()
            with open(os.path.join("mods", "devices.dat"),
                      "r", encoding="utf-8") as datafile:
                devices = datafile.read().strip()
                datafile.close()
            with open(os.path.join("mods", "running.dat"), "r", encoding="utf-8") as datafile:
                running = datafile.read().strip()
                datafile.close()
                if running:
                    running_time = datetime.datetime.strptime(running, "%Y-%m-%d %H:%M:%S.%f")
                    current_time = datetime.datetime.now()
                    if (current_time - running_time).total_seconds() > 30:
                        exiting = True
                        break
            sleep(15)
    except Exception as e:
        print(f"Error reading files: {e}")


try:
    exiting = False
    if not os.path.exists(os.path.join("mods", "rich_presence", "enabled.dat")):
        with open(os.path.join("mods", "rich_presence", "enabled.dat"), "w", encoding="utf-8") as f:
            f.write("1")
            f.close()
    if not os.path.exists(os.path.join("mods", "devices.dat")):
        with open(os.path.join("mods", "rich_presence", "devices.dat"), "w", encoding="utf-8") as f:
            f.write("0")
            f.close()
    with open(os.path.join("mods", "rich_presence", "enabled.dat"), "r", encoding="utf-8") as f:
        enabled_rich_presence = f.read().strip() == "1"
        f.close()
    with open(os.path.join("mods", "devices.dat"), "r", encoding="utf-8") as f:
        devices = f.read().strip()
        f.close()
    Thread(target=update_vars, daemon=True).start()
    start = int(time())
    while not exiting:
        if enabled_rich_presence:
            client_id = "REDACTED"  # Replace with your actual Discord client ID
            RPC = Presence(client_id)
            RPC.connect()
            RPC.update(state="Connected to " + str(devices) + " devices in "
                             "OpenADB Shell! Download here: "
                             "https://github.com/lukbrew25/openadbshell",
                       start=start)
            sleep(15)
            while not exiting:
                if not enabled_rich_presence:
                    RPC.close()
                    break
                RPC.update(state="Connected to " + str(devices) +
                                 " device(s) in OpenADB Shell! Download here: "
                                 "https://github.com/lukbrew25/openadbshell",
                           start=start)
                sleep(15)
        sleep(30)
except Exception as e:
    print(f"Error in Rich Presence: {e}")

sys.exit(0)
