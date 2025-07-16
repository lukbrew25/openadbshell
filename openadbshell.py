import subprocess
import sys
import os

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

print("Welcome to the OpenADB Shell!")
print("Type 'help' for a list of commands or type standard adb commands directly without the adb prefix.")
print("--------------------------------------------")
print("Created by lukbrew25")
print("Fully open source software, available on GitHub")
print("https://github.com/lukbrew25/openadbshell")
print("--------------------------------------------")
if not os.path.exists("adb\\adb.exe"):
    print("ADB executable not found in 'adb' directory. Please ensure you have the android platform tools files in the adb folder.")
    sys.exit(1)
run_and_stream_command("adb\\adb.exe version")
print("--------------------------------------------")

while True:
    user_command = str(input("openadbshell:"))
    if user_command.lower() == "exit":
        print("Exiting adb shell.")
        sys.exit(0)
    elif user_command.lower() == "clear":
        os.system('cls')
    elif user_command.lower() == "help":
        print("Available commands:")
        print("  exit - Exit the adb shell")
        print("  clear - Clear the console")
        print("  help - Show this help message")
        print("  localconnect - Connect to a local adb server by only port")
        print("  localdisconnect - Disconnect from a local adb server by only port")
        print("  wsaconnect - Connect to local default WSA adb port (58526).")
        print("  wsadisconnect - Disconnect from local default WSA adb port (58526).")
        print("  <adb command> - Execute an adb command")
    elif user_command.lower ()== "localconnect":
        port = input("Enter the port to connect to (default 5037): ")
        if not port.strip():
            port = "5037"
        run_command = "adb\\adb.exe connect localhost:" + str(port)
        run_and_stream_command(run_command)
    elif user_command.lower() == "localdisconnect":
        port = input("Enter the port to disconnect from (default 5037): ")
        if not port.strip():
            port = "5037"
        run_command = "adb\\adb.exe disconnect localhost:" + str(port)
        run_and_stream_command(run_command)
    elif user_command.lower() == "wsaconnect":
        run_command = "adb\\adb.exe connect localhost:58526"
        run_and_stream_command(run_command)
    elif user_command.lower() == "wsadisconnect":
        run_command = "adb\\adb.exe disconnect localhost:58526"
        run_and_stream_command(run_command)
    elif user_command.startswith("adb "):
        run_command = "adb\\adb.exe " + user_command[4:]
        run_and_stream_command(run_command)
    else:
        run_command = "adb\\adb.exe " + user_command
        run_and_stream_command(run_command)