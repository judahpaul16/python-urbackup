import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import dotenv_values
import urbackup

"""
Create a .env file in the tests directory and add the following lines to it:
URBACKUP_URL="http://your_urbackup_server:55414/x"
URBACKUP_USER="admin"
URBACKUP_PASSWORD="foo"
"""
config = dotenv_values()
server = urbackup.Server(config["URBACKUP_URL"], config["URBACKUP_USER"], config["URBACKUP_PASSWORD"], htpasswd=True)

for action in server.get_actions():
    a = action["action"]
    if a ==server.action_full_file or a==server.action_resumed_full_file:
        print("Running full file backup: "+action["name"])
        
        print("Stopping...")
        server.stop_action(action)