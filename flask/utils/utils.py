# Imports
import os
import time
import requests

# Get list of all .mp4 files
def getListOfFiles(dir_path):
    # create a list of file and sub directories 
    # names in the given directory 
    list_of_files = os.listdir(dir_path)
    all_files = list()

    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_path, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(full_path):
            all_files = all_files + getListOfFiles(full_path)
        else:
            all_files.append(full_path)

    # Filter to only new .mp4 files
    video_files = [i for i in all_files if i.endswith('.mp4')]       
    only_new_files = [i for i in video_files if not i.endswith('-saved.mp4')]
    
    return only_new_files

# Notify users with image
def notify(image_url):
    iftt_webhook(image_url)

# IFTT Webhook
def iftt_webhook(image_url):
    IFTTT_WEBHOOK = os.getenv('IFTTT_WEBHOOK')

    # Send notification using IFTTT
    print('Sending notification using IFTTT')
    dataObj = {"value1" : image_url, "value2" : "Camera Name"}
    requests.post(IFTTT_WEBHOOK, data = dataObj)