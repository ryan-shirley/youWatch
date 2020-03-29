import os
import time

class Video:
    def __init__(self, file_path):
        self.path = file_path
        self.name = os.path.basename(file_path)

    # Check if file has finished saving
    def check_if_fully_saved(self):
        file_path = self.path

        init_file_size = os.path.getsize(file_path)
        # print("Initial file size:", init_file_size)

        # Wait 3 seconds
        time.sleep(3)

        final_file_size = os.path.getsize(file_path)
        # print("Final file size:", final_file_size)

        # Check for difference in file size
        if init_file_size == final_file_size:
            return True
        else:
            return False

    # Rename file as saved
    def mark_as_saved(self):
        # Rename file
        new_file_path = self.path.replace(".mp4", "-saved.mp4")
        os.rename(self.path, new_file_path)

        # Update object
        self.name = self.name.replace(".mp4", "-saved.mp4")
        self.path = new_file_path

        return self

    # Analyse Video
    def analyse(self):
        print('Analysing video file')

        # Simulate analysis
        time.sleep(5)

        return self