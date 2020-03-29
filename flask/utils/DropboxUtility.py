import pathlib
import dropbox
import re
import os
from utils import notify

# Create a dropbox object using an API v2 key
API_KEY = os.getenv('DROPBOX_API_KEY')
d = dropbox.Dropbox(API_KEY)

class DropboxUtility:
    def __init__(self, folder, filename):
        self.folder = pathlib.Path(folder)    # located in this folder
        self.filename = filename         # file name
        self.filepath = self.folder / self.filename  # path object, defining the file
        self.target = "/Notification Thumbnails/"              # the target folder
        self.targetfile = self.target + self.filename   # the target path and file name

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
        
        notify(dl_url)