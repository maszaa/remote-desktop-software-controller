# remote-desktop-software-controller
Control desktop software running on your computer via web page.

**DISCLAIMER:** If you **execute, setup and use** this software it will operate on the windows that are open at the computer it is running on and **are configured to the database**. Other windows are not accesses but be careful which windows and commands you configure.


## Features

- You can define windows for softwares, command groups for windows, and commands for command groups. Command can have `free_text` which is sent as is to the software window in question. Command can also have a reference to a `Key` element and a `multiplier`. This causes `Key.key` to be sent `multiplier` times to the software window. If key reference exists it is preferred over `free_text`.
- You can define a position (X, Y from bottom-left origin) inside window as percentage which is clicked before sending keys. This can be set to all commands (set to Window) and each command may override these values.
- After defining commands you can send your keyboard key combinations to the software window by clicking buttons.
- You can click the screenshot of the software window. That click is forwarded to the actual software window.
- You can use mouse drag on desktop devices or move touch on mobile devices over the screenshot. That is forwarded as mouse drag to the actual software window.
- You can switch between "show commands" and "screenshot only" modes. In the later the command buttons are hidden. It also causes the viewport scale to be set to 1.0 on mobile devices and disables zooming to prevent user from zooming the page, going over the sceenshot and not being able to zoom out or scroll to the top of the view as `preventDefault` is called for touch events to prevent the screenshot image moving while capturing touch movement. "Show commands" is the default mode on page load.
- You can disable click and drag actions. By default those are enabled. When those are enabled the screenshot has a blue border. When disabled, the border doesn't have a border.
- If only one software window is configured the software window list view takes user to the control view of that sole window.


## Requirements
- Windows
- Python
- AutoHotkey


## Installation
1. Install AutoHotkey: https://www.autohotkey.com/
2. Download a release from releases page.
3. Double-click the downloaded `.exe` file.
4. Select path to extract to. RDSC will be extracted inside that to corresponding release directory.
5. Navigate to the extracted folder and double-click `RDSC.exe`.
6. Superuser will be created on first run, follow instructions.
7. Go to `http://<your LAN IP>:/admin/`, login and setup your softwares. More documentation on that TBA. You can though load an example from `examples` directory and investigate.
8. List of available software windows is available at `http://<your LAN IP>/`. You must login to access.

`RDSC.exe` has other commands available as well. Open Git Bash or Powershell, execute the exe and give it `--help` argument.

### Enable on startup

1. Create a shortcut for `RDSC.exe`.
2. Press `Windows` + `R` on your keyboard
3. Then write `shell:startup` and hit `Enter`
4. Folder for shortcuts to be executed in the Windows startup should open
5. Copy thw shortcut to Windows startup folder
6. Restart your computer to check if the configuration works. The server should now start at Windows startup.


## Development installation
1. Install AutoHotkey: https://www.autohotkey.com/
2. Install Python 3.8 (3.6 and 3.7 might work as well)
3. `git clone https://github.com/maszaa/remote-desktop-software-controller.git`
4. `cd remote-desktop-software-controller`
5. Create virtualenv: `python -m venv virtualenv`
6. Install Python dependencies:
    1. `pip install -r dev.requirements.txt`
    2. `pip install -r requirements.txt`
7. Activate virtualenv: `.\virtualenv\Scripts\Activate.ps1` (assuming you use Powershell)
8. `cd app`
9. Migrate database: `python manage.py migrate`
10. Create superuser: `python manage.py createsuperuser`
11. Start web server: `python manage.py <IP of your network adapter, 0.0.0.0 for LAN access>:<port>`
12. Go to `http://<your selected IP>:<your port>/admin/`, login and setup your softwares. More documentation on that TBA. You can though load an example from `examples` directory and investigate.
13. List of available software windows is available at `http://<your selected IP>:<your port>/`. You must login to access.

### Enable on startup

One possible option is at `scripts/start.sh`

There is also PowerShell version at `scripts/start.ps1`

1. You must have Git (Bash) installed on your computer
2. Press `Windows` + `R` on your keyboard
3. Then write `shell:startup` and hit `Enter`
4. Folder for shortcuts to be executed in the Windows startup should open
5. Open `scripts` folder and create a shortcut for `start.sh`
6. Copy that shortcut to Windows startup folder
7. Restart your computer to check if the configuration works. The server should now start at Windows startup. It also fetches the latest version from Git repository, executes database migrations and installs all Python dependencies.


## Documentation

For how each model is related to each other take a look at https://github.com/maszaa/remote-desktop-software-controller/tree/master/docs/rdsc_class_diagram.png

`Software.slug_name` and `Window.slug_title` are auto-generated after you hit save in Django Admin. Your edits will be overwritten.


## TODO

- Instructions how to setup a software window and its commands

### Wishlist / Nice to have

- Tests?
- More attractive UI?
