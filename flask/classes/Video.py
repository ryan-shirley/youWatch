# Utilities
import os
import time

# Object Detection
import cv2

class Video:
    def __init__(self, file_path):
        self.path = file_path
        self.name = os.path.basename(file_path)
        self.frame_generated_path = "./files/generated-frames/"

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

    # Generate frame from video
    def generate_frame(self, cam, currentframe):
        # reading from frame 
        ret,frame = cam.read() 

        if ret: 
            # If video has more frames
            name = self.frame_generated_path + 'frame-' + str(currentframe) + '.jpg'

            # Resize
            # height , width , layers =  frame.shape
            # new_h = round(height/2)
            # new_w = round(width/2)
            # resize = cv2.resize(frame, (new_w, new_h))

            cv2.imwrite(name, frame) 

            # Log
            # print("Video frame converted to .jpg - Path: " + name)

            return name
            
        else: 
            return False

    # Analyse Video
    def analyse_video(self):
        print('Analysing video file')

        # TODO: Clean old temporary files that might have been left over

        # Read the video from path
        cam = cv2.VideoCapture(self.path) 
        
        # Current frame number
        current_frame = 0
        
        # Loop through video file
        while(True): 
            
            # Generate indiviudal frame
            generated_frame = self.generate_frame(cam, current_frame)

            # Check if new frame was generated
            if generated_frame:

                # increasing counter so that it will 
                # show how many frames are created 
                current_frame += 1
            else:
                print("All frames generated.\nNo person was found!")
                break

        # Release all space and windows once done 
        cam.release() 
        cv2.destroyAllWindows() 
        
        return self