# youWatch
 CCTV Monitoring

## Environment Variables
| Variable          | Description                              | Example                                                |
|-------------------|------------------------------------------|--------------------------------------------------------|
| HOST_FILES        | Path to recording                        | /documents/NVR-Recordings/                             |
| HOST_MODELS       | Path to model                            | /documents/models                                      |
| DROPBOX_API_KEY   | API key to upload                        | xxxxxxx                                                |
| IFTTT_WEBHOOK     | Webhook Url                              | https://maker.ifttt.com/trigger/{event}/with/key/{key} |
| SLACK_WEBHOOK     | Webhook Url                              | https://hooks.slack.com/services/xxx                   |
| FAMILY_DEVICE_IPS | Name and ip address family members phone | Name-192.168.1.10 Name2-192.168.1.11                   |

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