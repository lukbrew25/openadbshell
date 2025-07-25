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
from time import sleep, time
import tkinter as tk
from tkinter import BooleanVar, messagebox
from tkinter import ttk
from threading import Thread
from pypresence import Presence


def save_config():
    """Save configuration to config.dat file."""
    try:
        with open("config.dat", "w", encoding="utf-8") as config_file:
            config_file.write(f"do_cust_command={do_cust_command}\n")
            config_file.write(f"rich_presence={rich_presence}\n")
            config_file.close()
    except Exception as e:
        print(f"Error saving config: {e}")


def load_config():
    """Load configuration from config.dat file."""
    global do_cust_command
    global rich_presence
    try:
        if os.path.exists("config.dat"):
            with open("config.dat", "r", encoding="utf-8") as config_file:
                for line in config_file:
                    line = line.strip()
                    if line.startswith("do_cust_command="):
                        value = line.split("=", 1)[1]
                        do_cust_command = value.lower() == "true"
                    if line.startswith("rich_presence="):
                        value = line.split("=", 1)[1]
                        rich_presence = value.lower() == "true"
                config_file.close()
        else:
            # Create config file with default value if it doesn't exist
            with open("config.dat", "w", encoding="utf-8") as config_file:
                config_file.write("do_cust_command=True\n")
                config_file.write("rich_presence=True\n")
                config_file.close()
    except Exception as e:
        print(f"Error loading config: {e}")


def load_saved_devices():
    """Load saved devices from config.dat file."""
    saved_devices = []
    try:
        if os.path.exists("config.dat"):
            with open("config.dat", "r", encoding="utf-8") as config_file:
                for line in config_file:
                    line = line.strip()
                    if line.startswith("saved_device="):
                        # Format: saved_device=name/!/ip:port or saved_device=name/!/ip:port/!/autoconnect
                        device_data = line.split("=", 1)[1]
                        if "/!/" in device_data:
                            parts = device_data.split("/!/")
                            if len(parts) >= 2:
                                name, ip_port = parts[0], parts[1]
                                # Check for autoconnect flag (backward compatibility)
                                autoconnect = False
                                if len(parts) >= 3:
                                    autoconnect = parts[2].lower() == "true"
                                saved_devices.append({
                                    "name": name,
                                    "ip_port": ip_port,
                                    "autoconnect": autoconnect
                                })
    except Exception as e:
        print(f"Error loading saved devices: {e}")
    return saved_devices


def save_saved_devices(devices):
    """Save devices to config.dat file, preserving other config entries."""
    try:
        # Read existing non-device config entries
        other_configs = []
        if os.path.exists("config.dat"):
            with open("config.dat", "r", encoding="utf-8") as config_file:
                for line in config_file:
                    line = line.strip()
                    if not line.startswith("saved_device="):
                        other_configs.append(line)

        # Write all config entries back
        with open("config.dat", "w", encoding="utf-8") as config_file:
            for config_line in other_configs:
                if config_line:  # Skip empty lines
                    config_file.write(f"{config_line}\n")
            for device in devices:
                autoconnect_str = "True" if device.get('autoconnect', False) else "False"
                config_file.write(f"saved_device={device['name']}/!/"
                                  f"{device['ip_port']}/!/{autoconnect_str}\n")
    except Exception as e:
        print(f"Error saving devices: {e}")


def clear_all_saved_devices():
    """Clear all saved devices immediately."""
    try:
        if os.path.exists("config.dat"):
            # Read existing non-device config entries
            other_configs = []
            with open("config.dat", "r", encoding="utf-8") as config_file:
                for line in config_file:
                    line = line.strip()
                    if not line.startswith("saved_device="):
                        other_configs.append(line)

            # Write back only non-device config entries
            with open("config.dat", "w", encoding="utf-8") as config_file:
                for config_line in other_configs:
                    if config_line:  # Skip empty lines
                        config_file.write(f"{config_line}\n")
        return True
    except Exception as e:
        print(f"Error clearing saved devices: {e}")
        return False


def open_config_window():  # pylint: disable=too-many-statements
    """Opens a configuration window to manage settings and saved devices."""
    global do_cust_command
    global rich_presence

    def save_and_close():
        global do_cust_command
        global rich_presence
        do_cust_command = var.get()
        rich_presence = rich_presence_var.get()
        save_config()

        # Save devices from the table
        devices = []
        for item in device_tree.get_children():
            values = device_tree.item(item, 'values')
            if len(values) >= 2 and values[0] and values[1]:
                autoconnect = False
                if len(values) >= 3:
                    autoconnect = values[2].upper() == 'Y'
                devices.append({
                    "name": values[0],
                    "ip_port": values[1],
                    "autoconnect": autoconnect
                })
        save_saved_devices(devices)

        config_win.destroy()

    def clear_all_devices():
        """Clear all saved devices immediately."""
        result = messagebox.askyesno("Confirm Clear",
                                     "Are you sure you want to clear all saved "
                                     "devices? This action cannot be undone.")
        if result:
            if clear_all_saved_devices():
                # Clear the tree view
                for item in device_tree.get_children():
                    device_tree.delete(item)
                messagebox.showinfo("Success",
                                    "All saved devices have been cleared.")
            else:
                messagebox.showerror("Error", "Failed to clear saved devices.")

    def add_device():
        """Add a new empty row to the device table."""
        device_tree.insert('', 'end', values=('', '', 'N'))

    def delete_selected_device():
        """Delete the selected device from the table."""
        selected_items = device_tree.selection()
        for item in selected_items:
            device_tree.delete(item)

    config_win = tk.Tk()
    config_win.title("OpenADB Config")
    config_win.geometry("600x500")
    config_win.resizable(True, True)

    # Custom commands section
    cmd_frame = tk.Frame(config_win)
    cmd_frame.pack(fill=tk.X, padx=10, pady=5)

    var = BooleanVar(value=do_cust_command)
    chk = tk.Checkbutton(cmd_frame, text="Enable custom command set", variable=var)
    chk.pack(anchor=tk.W)

    rich_presence_var = BooleanVar(value=rich_presence)
    rich_presence_chk = tk.Checkbutton(cmd_frame, text="Enable Rich Presence",
                                        variable=rich_presence_var)
    rich_presence_chk.pack(anchor=tk.W)

    # Saved devices section
    devices_frame = tk.LabelFrame(config_win, text="Saved Devices", padx=5, pady=5)
    devices_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Device table
    columns = ('Name', 'IP:Port', 'Autoconnect')
    device_tree = ttk.Treeview(devices_frame, columns=columns, show='headings',
                               height=10)

    # Configure columns
    device_tree.heading('Name', text='Device Name')
    device_tree.heading('IP:Port', text='IP Address:Port')
    device_tree.heading('Autoconnect', text='Autoconnect')
    device_tree.column('Name', width=150)
    device_tree.column('IP:Port', width=150)
    device_tree.column('Autoconnect', width=100)

    # Scrollbar for the tree
    scrollbar = ttk.Scrollbar(devices_frame, orient=tk.VERTICAL,
                              command=device_tree.yview)
    device_tree.configure(yscrollcommand=scrollbar.set)

    # Pack tree and scrollbar
    device_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Load existing saved devices
    saved_devices = load_saved_devices()
    for device in saved_devices:
        autoconnect_display = "Y" if device.get('autoconnect', False) else "N"
        device_tree.insert('', 'end', values=(device['name'], device['ip_port'], autoconnect_display))

    # Device management buttons
    device_btn_frame = tk.Frame(devices_frame)
    device_btn_frame.pack(fill=tk.X, pady=5)

    add_btn = tk.Button(device_btn_frame, text="Add Device", command=add_device)
    add_btn.pack(side=tk.LEFT, padx=5)

    delete_btn = tk.Button(device_btn_frame, text="Delete Selected",
                           command=delete_selected_device)
    delete_btn.pack(side=tk.LEFT, padx=5)

    clear_btn = tk.Button(device_btn_frame, text="Clear All (Immediate)",
                          command=clear_all_devices, bg='#ffcccc')
    clear_btn.pack(side=tk.LEFT, padx=5)

    # Make cells editable
    def on_double_click(event):
        """Handle double-click to edit cells."""
        region = device_tree.identify_region(event.x, event.y)
        if region == "cell":
            column = device_tree.identify_column(event.x)
            item = device_tree.identify('row', event.x, event.y)

            if item:
                col_index = int(column.replace('#', '')) - 1
                if col_index in [0, 1, 2]:  # Allow editing Name, IP:Port, and Autoconnect
                    edit_cell(item, col_index)

    def edit_cell(item, col_index):
        """Create an entry widget to edit the cell."""
        bbox = device_tree.bbox(item, column=col_index)
        if not bbox:
            return
        x, y, width, height = bbox

        values = device_tree.item(item, 'values')
        if col_index >= len(values):
            return
        current_value = values[col_index]

        # Special handling for autoconnect column (toggle Y/N)
        if col_index == 2:  # Autoconnect column
            new_value = 'Y' if current_value.upper() != 'Y' else 'N'
            values = list(device_tree.item(item, 'values'))
            values[col_index] = new_value
            device_tree.item(item, values=values)
            return

        # Regular text entry for other columns
        entry = tk.Entry(device_tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, current_value)
        entry.focus()

        def save_edit(event=None):  # pylint: disable=unused-argument
            new_value = entry.get()
            values = list(device_tree.item(item, 'values'))
            values[col_index] = new_value
            device_tree.item(item, values=values)
            entry.destroy()

        def cancel_edit(event=None):  # pylint: disable=unused-argument
            entry.destroy()

        entry.bind('<Return>', save_edit)
        entry.bind('<Escape>', cancel_edit)
        entry.bind('<FocusOut>', save_edit)

    device_tree.bind('<Double-1>', on_double_click)

    # Bottom buttons
    btn_frame = tk.Frame(config_win)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)

    save_btn = tk.Button(btn_frame, text="Save", command=save_and_close)
    save_btn.pack(side=tk.LEFT, padx=5)

    exit_btn = tk.Button(btn_frame, text="Cancel", command=config_win.destroy)
    exit_btn.pack(side=tk.LEFT, padx=5)

    # Instructions
    instructions = tk.Label(config_win,
                            text="Double-click cells to edit. Click Autoconnect column to toggle Y/N. "
                                 "Use 'Save' to apply table changes, 'Clear All' takes "
                                 "immediate effect.",
                            font=('Arial', 8), fg='gray')
    instructions.pack(side=tk.BOTTOM, pady=5)

    config_win.mainloop()


def autoconnect_on_startup():
    """Connect to devices with autoconnect enabled on startup."""
    global devices
    try:
        saved_devices = load_saved_devices()
        for device in saved_devices:
            if device.get('autoconnect', False):
                print(f"Auto-connecting to {device['name']} ({device['ip_port']})...")
                run_command = f"adb\\adb.exe connect {device['ip_port']}"
                if run_and_stream_command(run_command):
                    devices += 1
                    print(f"Successfully auto-connected to {device['name']}")
                else:
                    print(f"Failed to auto-connect to {device['name']}")
    except Exception as e:
        print(f"Error during autoconnect: {e}")


def do_rich_presence(enabled_rich_presence):
    """
    Initializes and updates the Rich Presence for Discord.
    """
    global devices
    try:
        while True:
            if enabled_rich_presence:
                client_id = "REDACTED"  # Replace with your actual Discord client ID
                RPC = Presence(client_id)
                RPC.connect()
                start = int(time())
                RPC.update(state="Connected to 0 devices in OpenADB Shell! Download here: "
                                                                "https://github.com/lukbrew25/openadbshell",
                           start=start)
                sleep(15)
                while True:
                    RPC.update(state="Connected to " + str(devices) + " device(s) in OpenADB Shell! Download here: "
                                                                    "https://github.com/lukbrew25/openadbshell",
                               start=start)
                    sleep(15)
            sleep(30)
    except Exception as e:
        print(f"Error in Rich Presence: {e}")


def run_and_stream_command(command):
    """
    Executes a given command and streams its stdout and stderr to the console.

    Args:
        command (str): The command string to execute.
    """
    try:
        success = True
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
            if "cannot" in line.lower():
                success = False

        for line in iter(process.stderr.readline, ''):
            print(f"Error: {line}", end='')
            if "cannot" in line.lower():
                success = False

        process.wait()
        return success
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


try:
    if not os.path.exists("config.dat"):
        with open("config.dat", "w", encoding="utf-8") as f:
            f.write("do_cust_command=True\n")
            f.write("rich_presence=True\n")
            f.close()
except Exception as e:
    print(f"Error creating config file: {e}")

devices = 0
do_cust_command = True
rich_presence = True
load_config()
doing_rich_presence = Thread(target=do_rich_presence, args=(rich_presence,))
doing_rich_presence.start()
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

# Auto-connect to saved devices with autoconnect enabled
autoconnect_on_startup()
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
            devices = 0
        print("Exiting adb shell.")
        sys.exit(0)
    elif do_cust_command and user_command.lower() == "clear":
        os.system('cls')
    elif do_cust_command and user_command.lower() == "help":
        print("Available commands:")
        print("  config - Open the configuration window to enable/disable "
              "custom commands and manage saved devices with autoconnect")
        print("  exit - Exit the adb shell")
        print("  clear - Clear the console")
        print("  help - Show this help message")
        print("  save ip:port --name <name> - Save a device connection with a name")
        print("  removesaved <name> - Remove a saved device by name")
        print("  connectsaved <name> - Connect to a saved device by name")
        print("  disconnectsaved <name> - Disconnect from a saved device by name")
        print("  installedapps - List installed apps on connected devices")
        print("  apppath <com.example.example> - Show the path to the apk file")
        print("  localconnect <port> - Connect to a local adb server by only port")
        print("  localdisconnect <port> - Disconnect from "
              "a local adb server by only port")
        print("  wsaconnect - Connect to local default WSA adb port (58526).")
        print("  wsadisconnect - Disconnect from local default WSA adb port (58526).")
        print("  shpm <command> - Execute a shell pm command on the device.")
        print("  <adb command> - Execute an adb command")
        print("")
        print("Note: Devices with autoconnect enabled will automatically connect on startup.")
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
        if run_and_stream_command(run_command):
            devices +=1
    elif do_cust_command and user_command.lower().startswith("localdisconnect "):
        port = user_command[16:].strip()
        if not port.isdigit():
            if port.lower() == "wsa":
                port = "58526"
            else:
                print("Error: Please provide a valid port number.")
                continue
        run_command = "adb\\adb.exe disconnect localhost:" + str(port)
        if run_and_stream_command(run_command):
            devices -= 1
            if devices < 0:
                devices = 0
    elif do_cust_command and user_command.lower() == "wsaconnect":
        run_command = "adb\\adb.exe connect localhost:58526"
        if run_and_stream_command(run_command):
            devices += 1
    elif do_cust_command and user_command.lower() == "wsadisconnect":
        run_command = "adb\\adb.exe disconnect localhost:58526"
        if run_and_stream_command(run_command):
            devices -= 1
            if devices < 0:
                devices = 0
    elif do_cust_command and user_command.lower() == "connect wsa":
        run_command = "adb\\adb.exe connect localhost:58526"
        if run_and_stream_command(run_command):
            devices += 1
    elif do_cust_command and user_command.lower() == "disconnect wsa":
        run_command = "adb\\adb.exe disconnect localhost:58526"
        if run_and_stream_command(run_command):
            devices -= 1
            if devices < 0:
                devices = 0
    elif do_cust_command and user_command.lower().startswith("save "):
        parts = user_command[5:].strip().split("--name")
        if len(parts) != 2:
            print("Error: Please provide an IP:port and a name for the saved device.")
            continue
        ip_port = parts[0].strip()
        name = parts[1].strip()
        if not ip_port or not name:
            print("Error: Please provide both IP:port and a name.")
            continue
        with open("config.dat", "a", encoding="utf-8") as f:
            f.write(f"saved_device={name}/!/{ip_port}/!/False\n")
            f.close()
    elif do_cust_command and user_command.lower().startswith("removesaved "):
        name = user_command[10:].strip()
        if not name:
            print("Error: Please provide a name for the saved device.")
            continue
        try:
            with open("config.dat", "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            with open("config.dat", "w", encoding="utf-8") as f:
                for line in lines:
                    if not line.startswith(f"saved_device={name}/!/"):
                        f.write(line)
            print(f"Removed saved device '{name}'.")
        except Exception as e:
            print(f"Error removing saved device: {e}")
    elif do_cust_command and user_command.lower().startswith("connectsaved "):
        name = user_command[13:].strip()
        if not name:
            print("Error: Please provide a name for the saved device.")
            continue
        try:
            with open("config.dat", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(f"saved_device={name}/!/"):
                        parts = line.strip().split("/!/")
                        if len(parts) >= 2:
                            ip_port = parts[1]
                            run_command = f"adb\\adb.exe connect {ip_port}"
                            run_and_stream_command(run_command)
                            break
                else:
                    print(f"Error: No saved device found with name '{name}'.")
                f.close()
        except Exception as e:
            print(f"Error reading config.dat: {e}")
    elif do_cust_command and user_command.lower().startswith("disconnectsaved "):
        name = user_command[16:].strip()
        if not name:
            print("Error: Please provide a name for the saved device.")
            continue
        try:
            with open("config.dat", "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith(f"saved_device={name}/!/"):
                        parts = line.strip().split("/!/")
                        if len(parts) >= 2:
                            ip_port = parts[1]
                            run_command = f"adb\\adb.exe disconnect {ip_port}"
                            run_and_stream_command(run_command)
                            break
                else:
                    print(f"Error: No saved device found with name '{name}'.")
                f.close()
        except Exception as e:
            print(f"Error reading config.dat: {e}")
    elif do_cust_command and user_command.lower().startswith("shpm "):
        run_command = "adb\\adb.exe shell pm " + user_command[5:]
        run_and_stream_command(run_command)
    elif (user_command.startswith("connect ") or user_command.startswith("adb connect ")
          or user_command.startswith("adb.exe connect ")):
        if user_command.startswith("connect "):
            run_command = "adb\\adb.exe connect " + user_command[8:]
        elif user_command.startswith("adb connect "):
            run_command = "adb\\adb.exe connect " + user_command[12:]
        else:
            run_command = "adb\\adb.exe connect " + user_command[16:]
        if run_and_stream_command(run_command):
            devices += 1
    elif (user_command.startswith("disconnect ") or user_command.startswith("adb disconnect ")
          or user_command.startswith("adb.exe disconnect ")):
        if user_command.startswith("disconnect "):
            run_command = "adb\\adb.exe disconnect " + user_command[11:]
        elif user_command.startswith("adb disconnect "):
            run_command = "adb\\adb.exe disconnect " + user_command[15:]
        else:
            run_command = "adb\\adb.exe disconnect " + user_command[19:]
        if run_and_stream_command(run_command):
            devices -= 1
            if devices < 0:
                devices = 0
    elif user_command.startswith("adb "):
        run_command = "adb\\adb.exe " + user_command[4:]
        run_and_stream_command(run_command)
    elif user_command.startswith("adb.exe "):
        run_command = "adb\\adb.exe " + user_command[8:]
        run_and_stream_command(run_command)
    else:
        run_command = "adb\\adb.exe " + user_command
        run_and_stream_command(run_command)
