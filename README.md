# remote-desktop-software-controller
Control desktop software running on your computer via web

**DISCLAIMER:** If you <u>execute, setup and use</u> this software it will operate on the windows that are open at the computer it is running on and are configured to the database. Be careful which windows and commands you configure.

## Requirements
- Windows
- Python
- AutoHotkey


## Installation
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
7. Create superuser: `python manage.py createsuperuser`
8. Start web server: `python manage.py <IP of your network adapter, 0.0.0.0 for LAN access>:<port>`
9. Go to `http://<your selected IP>:<your port>/admin/`, login and setup your softwares. More documentation on that TBA. You can though load an example from `examples` directory and investigate.


## TODO
- Render a screenshot of the current state of the software window at the software window page
- Instructions to data model, how to setup
- Improve error handling
- Authentication?
- Restricted access, by IP for example?
