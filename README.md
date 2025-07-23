# OpenADB Shell

OpenADB Shell is a simple, open source command-line interface for interacting with ADB (Android Debug Bridge) on Windows. It provides a user-friendly shell with custom commands, configuration options, and direct access to standard ADB commands.

<img width="2177" height="1202" alt="image" src="https://github.com/user-attachments/assets/aeb1044a-9861-424f-be07-15fd2a5d7810" />

## Features
- Run any standard ADB command (no need to prefix with `adb.exe`)
- Custom commands for common tasks (list apps, connect/disconnect, clear, etc.)
- Configuration window to enable/disable custom commands
- Persistent configuration saved to `config.dat`
- Error handling for missing ADB tools
- Open source and easy to extend

## Installation
1. Download the latest release zip from [GitHub Releases](https://github.com/lukbrew25/openadbshell/releases).
2. Unzip the file into a folder (e.g., your Documents folder).
3. Download the latest Android SDK Platform Tools for Windows: [Platform Tools Download](https://developer.android.com/tools/releases/platform-tools)
4. In your `openadbshell` directory, create a folder named `adb`.
5. Unzip the platform tools and move all files directly into the `adb` folder (so you have `adb/adb.exe`, etc.).
6. Run `openadbshell.exe` to start the shell.

Your directory structure should look like (ignoring the internal files):

```
openadbshell/
  openadbshell.exe
  adb/
    adb.exe
    ...other platform tools files...
```

## Adding to Windows Terminal
1. Follow the installation steps above.
2. Open Windows Terminal > Settings > Add a new profile (duplicate Command Prompt).
3. Set the name to "OpenADB Shell".
4. Set the command line executable to the path of `openadbshell.exe`.
5. Set the starting directory to your `openadbshell` folder.
6. Save and launch from Windows Terminal.

## Usage
- Type `help` for a list of available custom commands.
- Type any standard ADB command (without the `adb.exe` prefix) to run it directly.
- Type `config` to open the configuration window and enable/disable custom commands and manage custom devices saved.
- If custom commands are disabled, only standard ADB commands will work (except `config`).

## Available Shell-Specific Commands (run help for more info)
| Command                      | Description                                        |
|------------------------------|----------------------------------------------------|
| config                       | Open the configuration window                      |
| exit                         | Exit the shell (optionally disconnect all devices) |
| clear                        | Clear the console                                  |
| help                         | Show this help message                             |
| save <ip:port> --name <name> | Save the current ADB connection to a callable name |
| connectsaved <name>          | Load a saved ADB connection by name                |
| disconnect saved <name>      | Disconnect a saved ADB connection by name          |
| removesaved <name>           | Remove a saved connection by name                  |
| installedapps                | List installed apps on connected devices           |
| apppath <package>            | Show the path to the APK file for a package        |
| localconnect <port>          | Connect to a local ADB server by port              |
| localdisconnect <port>       | Disconnect from a local ADB server by port         |
| wsaconnect                   | Connect to the default WSA ADB port (58526)        |
| wsadisconnect                | Disconnect from the default WSA ADB port (58526)   |
| connect wsa                  | Alias for wsaconnect                               |
| disconnect wsa               | Alias for wsadisconnect                            |
| shpm <command>               | Execute a shell pm command on the device           |
| adb <args>                   | Run any ADB command (with or without the prefix)   |

## Configuration
- The shell saves your custom command preference in `config.dat`.
- You can change this at any time by running the `config` command.

## Requirements
- Windows OS
- Android SDK Platform Tools (in the `adb` folder)
- Python (for running the script directly) or use the provided EXE

## License
See [LICENSE](LICENSE).

**Not affiliated with Android, Google, Microsoft, or Windows.**

---

Created by lukbrew25  
