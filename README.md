# youWatch
 CCTV Monitoring


## Local Setup

### 1. Run Redis Worker
`cd deep-learning`
`source env/bin/activate`
`python3 -u worker.py`

### 2. Run File Watcher
`cd deep-learning`
`source env/bin/activate`
`python3 run_watcher.py`

### 3. Run Redis Server
`redis-server`

### 4. Run Flask Sever
`cd flask`
`source env/bin/activate`
`flask run`