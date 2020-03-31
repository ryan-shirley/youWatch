# Scheduler
import schedule

# Redis
import redis
from rq import Queue

# Others
import time
import datetime
from datetime import datetime as dt
import os

# Utils
from utils.utils import getListOfFiles
from dotenv import load_dotenv
load_dotenv()

# Custom classes
from classes.Video import Video
from ping3 import ping

# Redis Config
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)
q = Queue(connection=r)

# Check is anyone home?
def check_for_someone_home():
    # print('Checking if someone is home')

    # Get list of names and phone ip address
    family_phone_ips = os.getenv('FAMILY_DEVICE_IPS')
    family_phone_ips_list = [i.split("-") for i in family_phone_ips.split(" ")] 

    # Loop people to check if home
    for name, ip_address in family_phone_ips_list:
        HOST_UP = ping(ip_address, timeout=5)

        # Return if device is active
        if HOST_UP > 0:
            print(name + ' is home')
            return True

    # No one found at home
    print("No one is home")
    return False

# Check if a time in within range
def in_override_time():
    start = datetime.time(23, 0, 0)
    end = datetime.time(7, 0, 0)
    now = dt.now()
    now = now.strftime("%H:%M:%S")
    now = datetime.datetime.strptime(now, "%H:%M:%S").time()

    if start <= end:
        return start <= now <= end
    else:
        return start <= now or now <= end

# Check for new files
def check_new_files():
    print("Task: Checking for new files")

    dir_path = "./files/recordings"
    files = getListOfFiles(dir_path)

    # TODO: Move inside to only run if files are present
    # Check if time is in specified range for override
    override = in_override_time()
    print("Override even if someone is home ", override)

    # Check for if someone is home
    devices_registered = os.getenv('FAMILY_DEVICE_IPS', False)

    if devices_registered and not override:
        is_someone_home = check_for_someone_home()

    if len(files) > 0:

        # Add videos into request queue individualy if fully saved
        for file_path in files:
            video = Video(file_path)

            # Check file has fully saved
            is_finished_saving = video.check_if_fully_saved()

            # Check File has finished saving
            if is_finished_saving == True:
                video.mark_as_saved()

                print(f"Adding {video.name} to the queue to be analysed.")
                q.enqueue(video.analyse_video)

        print("Task: Completed checking for new files")
    else:
        print("No new video files")

# Add job to queue to check for new files
def job_check_new_files():
    print("Add new Job: Check files to queue")
    q.enqueue(check_new_files)

# Schedule Config
schedule.every(1).minutes.do(job_check_new_files)

# Inital function to run schedule
def intit_watcher():
    print('Init watcher on redis host:', redis_host)
    time.sleep(5)
    job_check_new_files()

    while True:
        schedule.run_pending()
        time.sleep(1)
