# HomeHelpdesk
A locally hosted 'helpdesk' i've build to track home tasks with email notifications

Prerequisites:
- A Raspberry Pi running Debian/Raspbian, connected to your local network
- A working iCloud account with Two-Factor Authentication and an App-Specific Password
- (Optional) A custom domain for your helpdesk email address
-  Basic familiarity with SSH, nano (or your editor), and the command line

<img width="1221" alt="Screenshot 2025-07-01 at 10 50 06 AM" src="https://github.com/user-attachments/assets/7b20038d-7407-4a2c-9757-7df2d5a7aa1c" />

Overall - pretty easy to get up and running if you follow the below steps:

1. System Update & Install Essentials
  sudo apt update && sudo apt upgrade -y
  sudo apt install python3-pip python3-venv nginx -y

2. Create Project Directory & Python Virtualenv
  mkdir -p ~/household-helpdesk
  cd ~/household-helpdesk
  python3 -m venv ~/flaskenv
  source ~/flaskenv/bin/activate
  pip install flask

3. Project Structure
   ~/household-helpdesk/
  ├── app.py
  ├── tickets.json
  ├── templates/
  │   ├── create.html
  │   ├── edit.html
  │   ├── index.html
  │   └── dashboard.html
  └── static/
      └── favicon.ico

4. Create the Data File
   echo '{"active":[],"completed":[],"deleted":[]}' > tickets.json

