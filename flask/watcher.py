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
from utils.analysis import analyse_file

# Redis Config
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)
q = Queue(connection=r)

# Check for new files
def check_new_files():
    print("\nTask: Checking for new files\n")

    dir_path = "./files/recordings"
    files = getListOfFiles(dir_path)

    if len(files) > 0:
        # TODO: Add files individualy into request queue
        for file_path in files:
            is_finished_saving = check_save_status(file_path)
            file_name = os.path.basename(file_path)

            # Check File has finished saving
            if is_finished_saving == True:
                print(f"Adding {file_name} to the queue to be analysed.")
                q.enqueue(analyse_file, file_path, file_name)

        print("\nTask: Completed checking for new files\n")
    else:
        print("No files")

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
