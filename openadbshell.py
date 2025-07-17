"""
This script is a simple command-line interface for
interacting with ADB (Android Debug Bridge).
"""
# pyinstaller --icon openadbshell.ico --add-data "LICENSE;."
# --add-data "README.MD;." --add-data "contributing.md;." openadbshell.py
# ico file not included in the repository, please create your own icon file
# and use it with the --icon flag.
import subprocess
import sys
import os
from time import sleep


def run_and_stream_command(command):
    """
    Executes a given command and streams its stdout and stderr to the console.

    Args:
        command (str): The command string to execute.
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        for line in iter(process.stdout.readline, ''):
            print(line, end='')

        for line in iter(process.stderr.readline, ''):
            print(f"Error: {line}", end='')

        process.wait()
    except Exception as e:
        print(f"An error occurred: {e}")


print("Welcome to the OpenADB Shell! (v1.0.1)")
print("Type 'help' for a list of shell-specific commands or type standard adb commands directly "
      "without the adb.exe prefix.")
print("--------------------------------------------")
print("Created by lukbrew25")
print("Fully open source software, available on GitHub")
print("https://github.com/lukbrew25/openadbshell")
print("--------------------------------------------")
if not os.path.exists("adb\\adb.exe"):
    print("ADB executable not found in 'adb' directory. Please ensure you have the android "
          "platform tools files in the adb folder.")
    sleep(5)
    sys.exit(1)
run_and_stream_command("adb\\adb.exe version")
print("--------------------------------------------")

while True:
    user_command = str(input("openadbshell:"))
    if user_command.lower() == "exit":
        disconnect = input("Would you like to disconnect from all devices before "
                           "exiting? (y/n): ")
        if disconnect.lower() == 'y':
            run_and_stream_command("adb\\adb.exe disconnect")
        print("Exiting adb shell.")
        sys.exit(0)
    elif user_command.lower() == "clear":
        os.system('cls')
    elif user_command.lower() == "help":
        print("Available commands:")
        print("  exit - Exit the adb shell")
        print("  clear - Clear the console")
        print("  help - Show this help message")
        print("  installedapps - List installed apps on connected devices")
        print("  apppath <com.example.example> - Show the path to the apk file")
        print("  localconnect <port> - Connect to a local adb server by only port")
        print("  localdisconnect <port> - Disconnect from "
              "a local adb server by only port")
        print("  wsaconnect - Connect to local default WSA adb port (58526).")
        print("  wsadisconnect - Disconnect from local default WSA adb port (58526).")
        print("  <adb command> - Execute an adb command")
    elif user_command.lower() == "installedapps":
        run_command = "adb\\adb.exe shell pm list packages"
        run_and_stream_command(run_command)
    elif user_command.startswith("apppath "):
        package_name = user_command[8:].strip()
        if not package_name:
            print("Error: Please provide a package name.")
            continue
        run_command = "adb\\adb.exe shell pm path " + str(package_name)
        run_and_stream_command(run_command)
    elif user_command.lower().startswith("localconnect "):
        port = user_command[13:].strip()
        if not port.isdigit():
            if port.lower() == "wsa":
                port = "58526"
            else:
                print("Error: Please provide a valid port number.")
                continue
        run_command = "adb\\adb.exe connect localhost:" + str(port)
        run_and_stream_command(run_command)
    elif user_command.lower().startswith("localdisconnect "):
        port = user_command[16:].strip()
        if not port.isdigit():
            if port.lower() == "wsa":
                port = "58526"
            else:
                print("Error: Please provide a valid port number.")
                continue
        run_command = "adb\\adb.exe disconnect localhost:" + str(port)
        run_and_stream_command(run_command)
    elif user_command.lower() == "wsaconnect":
        run_command = "adb\\adb.exe connect localhost:58526"
        run_and_stream_command(run_command)
    elif user_command.lower() == "wsadisconnect":
        run_command = "adb\\adb.exe disconnect localhost:58526"
        run_and_stream_command(run_command)
    elif user_command.lower() == "connect wsa":
        run_command = "adb\\adb.exe connect localhost:58526"
        run_and_stream_command(run_command)
    elif user_command.lower() == "disconnect wsa":
        run_command = "adb\\adb.exe disconnect localhost:58526"
        run_and_stream_command(run_command)
    elif user_command.startswith("adb "):
        run_command = "adb\\adb.exe " + user_command[4:]
        run_and_stream_command(run_command)
    else:
        run_command = "adb\\adb.exe " + user_command
        run_and_stream_command(run_command)
