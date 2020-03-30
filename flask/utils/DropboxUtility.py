import pathlib
import dropbox
import re
import os
import requests
import json

# Create a dropbox object using an API v2 key
API_KEY = os.getenv('DROPBOX_API_KEY')
d = dropbox.Dropbox(API_KEY)

class DropboxUtility:
    def __init__(self, folder, filename, created_at):
        self.folder = pathlib.Path(folder)    # located in this folder
        self.filename = filename         # file name
        self.filepath = self.folder / self.filename  # path object, defining the file
        self.target = "/Notification Thumbnails/"              # the target folder
        self.targetfile = self.target + self.filename   # the target path and file name
        self.created_at = created_at

    # Upload file to dropbox
    def upload(self):
        print('Uploading file to dropbox')

        # open the file and upload it
        with self.filepath.open("rb") as f:
            # upload gives you metadata about the file
            # we want to overwite any previous version of the file
            meta = d.files_upload(f.read(), self.targetfile, mode=dropbox.files.WriteMode("overwrite"))

        # create a shared link
        link = d.sharing_create_shared_link(self.targetfile)

        # url which can be shared
        url = link.url

        # link which directly downloads by replacing ?dl=0 with ?dl=1
        dl_url = re.sub(r"\?dl\=0", "?dl=1", url)
        
        self.notify(dl_url)

    # Notify users with image
    def notify(self, image_url):
        self.iftt_webhook(image_url)
        self.slack_webhook(image_url)

        return self

    # IFTT Webhook
    def iftt_webhook(self, image_url):
        IFTTT_WEBHOOK = os.getenv('IFTTT_WEBHOOK')

        # Send notification using IFTTT
        print('Sending notification using IFTTT')
        dataObj = {"value1" : image_url, "value2" : f"{self.created_at}"}
        requests.post(IFTTT_WEBHOOK, data = dataObj)

    # Slack Webhook
    def slack_webhook(self, image_url):
        SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK')

        # Send notification using Slack
        print('Sending notification using Slack')
        dataObj = {
            "blocks": [
            {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":warning: *Person found on camera*"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "text": f"*{self.created_at}*",
                            "type": "mrkdwn"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "image",
                    "image_url": f"{image_url}",
                    "alt_text": "image1"
                }
            ]
        }

        json_string = json.dumps(dataObj)

        r = requests.post(SLACK_WEBHOOK, data = json_string, headers={'Content-Type': 'application/json'})
        print("Respononse:",r.text)
