This is an open source adb shell for Windows only.

Instructions:
1. Grab the zip from the latest release.
2. Unzip the file directly into an area of your user's directory - I recommend unzipping the file into your documents folder.
3. Download the latest android SDK Platform Tools zip for windows from this link: https://developer.android.com/tools/releases/platform-tools
4. Open the "openadbshell" directory you unzipped and you should see the exe and an internal folder. Create another folder named "adb".
5. Unzip the sdk and move the individual files directly into the adb folder.
6. Now, you can run the openadbshell.exe to test out the shell.

Your installation should look like:

openadbshell>adb>adb.exe and other files

To add to windows 11 terminal:
1. Follow the above instructions.
2. Go to terminal>settings>add a new profile>duplicate current profile>duplicate command prompt profile.
3. Go to the new duplicated profile.
4. Change the name to "OpenADB Shell"
5. Change the command line executable to the openadbshell.exe
6. Set the starting directory to the openadbshell directory.
7. Now, you can access the shell from windows 11 terminal - just like cmd or powershell.

**Not affiliated with android, windows, google, or microsoft.
