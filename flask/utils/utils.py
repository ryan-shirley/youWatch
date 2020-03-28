# Imports
import os
import time

# Get list of all .mp4 files
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()

    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    video_files = [i for i in allFiles if i.endswith('.mp4')]            
    
    return video_files

# Check if file has finished saving
def check_save_status(file_path):
    init_file_size = os.path.getsize(file_path)
    # print("Initial file size:", init_file_size)

    # Wait 3 seconds
    time.sleep(3)

    final_file_size = os.path.getsize(file_path)
    # print("Final file size:", final_file_size)

    # Check for difference in file size
    if init_file_size == final_file_size:
        return True
    else:
        return False