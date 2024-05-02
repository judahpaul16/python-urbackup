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

clients = server.get_clients_with_group()

for client in clients:
    
    file_backups = server.get_clientbackups(client["id"])
    
    incr_file = 0
    full_file = 0
    
    for file_backup in file_backups:
        
        if file_backup["incremental"]>0:
            incr_file+=1
        else:
            full_file+=1
            
    incr_image = 0
    full_image = 0
    
    image_backups = server.get_clientimagebackups(client["id"])
    
    for image_backup in image_backups:
        
        if image_backup["letter"]=="SYSVOL" or image_backup["letter"]=="ESP":
            continue 
        
        if image_backup["incremental"]>0:
            incr_image+=1
        else:
            full_image+=1
            
    print("Client {clientname} in group {groupname} has {incr_file} incr file backups, {full_file} "
          "full file backups, {incr_image} incr image backups and "
          "{full_image} full image backups".format(
              incr_file=incr_file, clientname=client["name"],
              full_file=full_file, incr_image=incr_image,
              full_image=full_image, groupname=client["groupname"]) )
    
