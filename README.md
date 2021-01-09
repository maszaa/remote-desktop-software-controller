# remote-desktop-software-controller
Control desktop software running on your computer via web page.

**DISCLAIMER:** If you **execute, setup and use** this software it will operate on the windows that are open at the computer it is running on and **are configured to the database**. Other windows are not accesses but be careful which windows and commands you configure.


## Requirements
- Windows
- Python
- AutoHotkey


## Installation and usage
1. Install AutoHotkey
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
13. List of available software windows is available at `http://<your selected IP>:<your port>/`

### Enable on startup

One possible option is at `scripts/start.sh`

1. You must have Git (Bash) installed on your computer
2. Press `Windows` + `R` on your keyboard
3. Then write `shell:startup` and hit `Enter`
4. Folder for shortcuts to be executed in the Windows startup should open
5. Open `scripts` folder and create a shortcut for `start.sh`
6. Copy that shortcut to Windows startup folder
7. Restart your computer to check if the configuration works. The server should now start at Windows startup. It also fetches the latest version from Git repository, executes database migrations and installs all Python dependencies.


## Documentation

For how each model is related to each other take a look at https://github.com/maszaa/remote-desktop-software-controller/tree/master/docs/rdsc_class_diagram.png


## TODO

- Instructions how to setup a software window and its commands

### Wishlist / Nice to have

- Restricted access, by IP for example?
- Authentication?
- Tests?
- More attractive UI?
