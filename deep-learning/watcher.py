# Scheduler
import schedule

# Redis
import redis
from rq import Queue

# Others
import time
import os

# Utils
from utils.utils import getListOfFiles
from dotenv import load_dotenv
load_dotenv()

# Custom classes
from classes.Video import Video

# Redis Config
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)
q = Queue(connection=r)

# Check for new files
def check_new_files():
    print("Task: Checking for new files\n")

    dir_path = "./files/recordings"
    files = getListOfFiles(dir_path)

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

        print("\nTask: Completed checking for new files\n")
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
