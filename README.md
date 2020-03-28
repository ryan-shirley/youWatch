# youWatch
 CCTV Monitoring


## Local Setup

### 1. Run Redis Worker
`cd flask/`
`rq worker`

### 2. Run File Watcher
`source flask/env/bin/activate`
`python3 flask/run_wacther.py`

### 3. Run Redis Server
`redis-server`

### 5. Run File Watcher
`cd flask`
`source env/bin/activate`
`flask run`