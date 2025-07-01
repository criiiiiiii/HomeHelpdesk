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
   
  <img width="403" alt="Screenshot 2025-07-01 at 10 55 08 AM" src="https://github.com/user-attachments/assets/e04721d7-112b-4d53-aafb-20ee15b8461b" />


4. Create the Data File
   echo '{"active":[],"completed":[],"deleted":[]}' > tickets.json

5. app.py
Path: ~/household-helpdesk/app.py
Contents (replace placeholders with your real SMTP settings):

6. Templates
  templates/create.html
  templates/edit.html
  templates/index.html
  templates/dashboard.html
  
7. Favicon
  Create static/ and add your icon:
  mkdir -p ~/household-helpdesk/static
  # Copy your favicon.ico into that folder:
  # scp ~/Downloads/favicon.ico admin@<your-pi-ip>:/home/admin/household-helpdesk/static/favicon.ico

8. systemd Service
  Path: /etc/systemd/system/household-helpdesk.service
  [Unit]
  Description=Home Helpdesk Flask App
  After=network.target

  [Service]
  User=admin
  WorkingDirectory=/home/admin/household-helpdesk
  ExecStart=/home/admin/flaskenv/bin/python /home/admin/household-helpdesk/app.py
  Restart=always

 [Install]
 WantedBy=multi-user.target

  Enable & start:
  sudo systemctl daemon-reload
  sudo systemctl enable household-helpdesk.service
  sudo systemctl start household-helpdesk.service

9. Test & Access
  Create ticket: http://<your-pi-ip>:5080/create

  View tickets: http://<your-pi-ip>:5080/

  Dashboard: http://<your-pi-ip>:5080/dashboard



10. 
