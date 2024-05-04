from urbackup import installer_os, Server
import datetime
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import dotenv_values

"""
Create a .env file in the tests directory and add the following lines to it:
URBACKUP_URL="http://your_urbackup_server:55414/x"
URBACKUP_USER="admin"
URBACKUP_PASSWORD="foo"
"""
config = dotenv_values()
server = Server(config["URBACKUP_URL"], config["URBACKUP_USER"], config["URBACKUP_PASSWORD"], htpasswd=True)

for extra_client in server.get_extra_clients():  
    server.remove_extra_client(extra_client["id"])

computernames = """2.2.2.2
3.3.3.3"""

for line in computernames:
    server.add_extra_client(line)
        

clients = server.get_status()
usage = server.get_usage()

if len(clients) != len(usage):
    print("Failed to retreive usage or status information. Length of both lists is different.")

# Uncomment to format time differently
# locale.setlocale(locale.LC_TIME, "german")

diff_time = 3*24*60*60 # 3 days
for client in clients:
    
    if client["lastbackup"]=="-" or client["lastbackup"] < time.time() - diff_time:
        
        if client["lastbackup"]=="-" or client["lastbackup"]==0:
            lastbackup = "Never"
        else:
            lastbackup = datetime.datetime.fromtimestamp(client["lastbackup"]).strftime("%x %X")
            
        print("Last file backup at {lastbackup} of client {clientname} is older than three days".format(
              lastbackup=lastbackup, clientname=client["name"] ) )
        
        
#if server.start_incr_file_backup("Johnwin7test-PC2"):
#    print("Started file backup successfully")
#else:
#    print("Failed to start file backup")
    

if not server.get_livelog():
    print("Failed to get livelog contents")

settings = server.get_client_settings("Johnwin7test-PC2")

for key in settings:
    print("{key}={value}".format(key=key, value=settings[key]))
    
print("Authkey: "+server.get_client_authkey("Johnwin7test-PC2"))

if server.change_client_setting("Johnwin7test-PC2", "max_image_incr", "40"):
    print("Changed setting successfully")
else:
    print("Failed to change setting")
    
    
settings = server.get_global_settings()

for key in settings:
    print("Global: {key}={value}".format(key=key, value=settings[key]))
    

if server.set_global_setting("max_image_incr", "40"):
    print("Changed global setting successfully")
else:
    print("Failed to change global setting")

#Get all file backups for a specified client id
backups = server.get_clientbackups('8')

#Get all image backups for a specified client id
backups_image = server.get_clientimagebackups('8')

#Download a client installer
server.download_installer("test.exe", "test", installer_os.Windows)