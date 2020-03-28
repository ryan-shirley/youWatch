# Flask App
from app import app

# Redis
import redis
from rq import Queue

# Other
import time
import os

# Redis config
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, db=0)
q = Queue(connection=r)

# Background task
def background_task():
    print("Task running")

    print(f"Simulating a 2 second delay")
    time.sleep(2)

    print("Task complete")

    return

# Route to add new task to queue
@app.route("/task")
def task():
    job = q.enqueue(background_task)
    q_len = len(q)

    return f"Task ({job.id}) added to queue at {job.enqueued_at}. {q_len} tasks in the queue"
