# youWatch
 CCTV Monitoring


## Local Setup

### 1. Run Redis Worker
`cd flask/`
`rq worker`

### 2. Run File Watcher
`source flask/env/bin/activate`
`python3 flask/run_watcher.py`

### 3. Run Redis Server
`redis-server`

### 5. Run Flask Sever
`cd flask`
`source env/bin/activate`
`flask run`