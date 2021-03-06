import redis
from rq import Worker, Queue, Connection
import os
import time

from dotenv import load_dotenv
load_dotenv()

# Listening
listen = ['high', 'default', 'low']

# Redis server config
redis_host = os.getenv('REDIS_HOST', 'localhost')
conn = redis.from_url(f'redis://{redis_host}:6379')

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()