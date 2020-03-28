# Scheduler
import schedule

# Redis
import redis
from rq import Queue

# Others
import time
import os

# Redis Config
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)
q = Queue(connection=r)

# Check for new files
def check_new_files():
    print("Task: Checking for new files")

    # Simulate delay
    print('Simulating delay')
    time.sleep(4)

    print("Task: Completed checking for new files")

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