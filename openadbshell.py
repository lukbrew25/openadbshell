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
import tkinter as tk
from tkinter import BooleanVar


def save_config():
    """Save configuration to config.dat file."""
    try:
        with open("config.dat", "w", encoding="utf-8") as f:
            f.write(f"do_cust_command={do_cust_command}\n")
    except Exception as e:
        print(f"Error saving config: {e}")


def load_config():
    """Load configuration from config.dat file."""
    global do_cust_command
    try:
        if os.path.exists("config.dat"):
            with open("config.dat", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("do_cust_command="):
                        value = line.split("=", 1)[1]
                        do_cust_command = value.lower() == "true"
                        break
        else:
            # Create config file with default value if it doesn't exist
            with open("config.dat", "w", encoding="utf-8") as f:
                f.write("do_cust_command=True\n")
    except Exception as e:
        print(f"Error loading config: {e}")


def open_config_window():
    """Opens a configuration window to enable or disable custom commands."""
    global do_cust_command

    def save_and_close():
        global do_cust_command
        do_cust_command = var.get()
        save_config()
        config_win.destroy()

    config_win = tk.Tk()
    config_win.title("OpenADB Config")
    config_win.geometry("300x120")
    var = BooleanVar(value=do_cust_command)

    chk = tk.Checkbutton(config_win, text="Enable custom command set", variable=var)
    chk.pack(pady=10)

    btn_frame = tk.Frame(config_win)
    btn_frame.pack(pady=10)

    save_btn = tk.Button(btn_frame, text="Save", command=save_and_close)
    save_btn.pack(side=tk.LEFT, padx=10)

    exit_btn = tk.Button(btn_frame, text="Exit", command=config_win.destroy)
    exit_btn.pack(side=tk.LEFT, padx=10)

    config_win.mainloop()


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


do_cust_command = True
load_config()
print("Welcome to the OpenADB Shell! (v1.0.3)")
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
    if user_command.lower() == "config":
        open_config_window()
    elif do_cust_command and user_command.lower() == "exit":
        disconnect = input("Would you like to disconnect from all devices before "
                           "exiting? (y/n): ")
        if disconnect.lower().startswith('y'):
            run_and_stream_command("adb\\adb.exe disconnect")
        print("Exiting adb shell.")
        sys.exit(0)
    elif do_cust_command and user_command.lower() == "clear":
        os.system('cls')
    elif do_cust_command and user_command.lower() == "help":
        print("Available commands:")
        print("  config - Open the configuration window to enable/disable custom commands")
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
        print("  shpm <command> - Execute a shell pm command on the device.")
        print("  <adb command> - Execute an adb command")
    elif do_cust_command and user_command.lower() == "installedapps":
        run_command = "adb\\adb.exe shell pm list packages"
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.startswith("apppath "):
        package_name = user_command[8:].strip()
        if not package_name:
            print("Error: Please provide a package name.")
            continue
        run_command = "adb\\adb.exe shell pm path " + str(package_name)
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.lower().startswith("localconnect "):
        port = user_command[13:].strip()
        if not port.isdigit():
            if port.lower() == "wsa":
                port = "58526"
            else:
                print("Error: Please provide a valid port number.")
                continue
        run_command = "adb\\adb.exe connect localhost:" + str(port)
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.lower().startswith("localdisconnect "):
        port = user_command[16:].strip()
        if not port.isdigit():
            if port.lower() == "wsa":
                port = "58526"
            else:
                print("Error: Please provide a valid port number.")
                continue
        run_command = "adb\\adb.exe disconnect localhost:" + str(port)
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.lower() == "wsaconnect":
        run_command = "adb\\adb.exe connect localhost:58526"
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.lower() == "wsadisconnect":
        run_command = "adb\\adb.exe disconnect localhost:58526"
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.lower() == "connect wsa":
        run_command = "adb\\adb.exe connect localhost:58526"
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.lower() == "disconnect wsa":
        run_command = "adb\\adb.exe disconnect localhost:58526"
        run_and_stream_command(run_command)
    elif do_cust_command and user_command.lower().startswith("shpm "):
        run_command = "adb\\adb.exe shell pm " + user_command[5:]
        run_and_stream_command(run_command)
    elif user_command.startswith("adb "):
        run_command = "adb\\adb.exe " + user_command[4:]
        run_and_stream_command(run_command)
    else:
        run_command = "adb\\adb.exe " + user_command
        run_and_stream_command(run_command)
