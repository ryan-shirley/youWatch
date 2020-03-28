# Scheduler
import schedule

# Redis
import redis
from rq import Queue

# Others
import time
import os

# Utils
from utils.utils import getListOfFiles, check_save_status

# Redis Config
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)
q = Queue(connection=r)

# Check for new files
def check_new_files():
    print("\nTask: Checking for new files\n")

    dir_path = "./app/files/recordings"
    files = getListOfFiles(dir_path)

    # TODO: Add files individualy into request queue
    for file_path in files:
        is_finished_saving = check_save_status(file_path)
        file_name = os.path.basename(file_path)

        print(f"File {file_name} is finshed saving '{is_finished_saving}'.")

    print("\nTask: Completed checking for new files\n")
    return

# Add job to queue to check for new files
def job():
    q.enqueue(check_new_files)

# Schedule Config
schedule.every(1).minutes.do(job)

# Inital function to run schedule
def inti_watcher():
    print('Init watcher')

    while True:
        schedule.run_pending()
        time.sleep(1)
