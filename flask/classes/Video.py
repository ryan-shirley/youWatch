# Utilities
import os
import time

# Object Detection
import cv2
from imageai.Detection import ObjectDetection

# Set object detection model
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("./models/yolo.h5")
detector.loadModel()

class Video:
    def __init__(self, file_path):
        self.path = file_path
        self.name = os.path.basename(file_path)
        self.frame_generated_path = "./files/generated-frames/"
        self.frame_predictions_path = "./files/predicted-frames/"
        self.positive_matches = "./files/positive-matches/"
        self.false_positive_folder = "./files/false-positives/"
        self.detections = []

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

    # Move file to new folder
    def move_to_folder(self, new_path):
        # Generate new file path
        new_file_name = self.path.replace("-saved", '')
        new_file_path = new_file_name.replace("./files/recordings/", new_path)

        # Move file to new location
        os.rename(self.path, new_file_path)

        return new_file_path

    # Remove files created from analysis
    def clean_temporary_files(self):
        # Clean original
        originalfilelist = [ f for f in os.listdir(self.frame_generated_path) if f.endswith(".jpg") ]
        for f in originalfilelist:
            os.remove(os.path.join(self.frame_generated_path, f))
        
        # Clean analysed
        analysedfilelist = [ f for f in os.listdir(self.frame_predictions_path) if f.endswith(".jpg") ]
        for f in analysedfilelist:
            os.remove(os.path.join(self.frame_predictions_path, f))

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

    # Analyse individual frame
    def analyse_frame(self, frame_path):
        # Get path to where to save prediction
        output_path = frame_path.replace(self.frame_generated_path,self.frame_predictions_path)

        # print("Saving analysed frame.")
        detection = detector.detectObjectsFromImage(input_image=frame_path, output_image_path=output_path)

        # Loop through detections found
        detections = []
        for eachItem in detection:
            detections.append(eachItem["name"])
            # print(eachItem["name"] , " : ", eachItem["percentage_probability"])
        
        return detections

    # Analyse Video
    def analyse_video(self):
        print('Analysing video file')

        # TODO: Clean old temporary files that might have been left over

        # Read the video from path
        cam = cv2.VideoCapture(self.path) 
        
        # Current frame number
        current_frame_number = 0
        
        # Loop through video file
        while(True): 

            # Skip frames
            if current_frame_number > 0:
                for j in range(5):
                    ret,frame = cam.read() 

            # Generate indiviudal frame
            generated_frame_path = self.generate_frame(cam, current_frame_number)

            # Check if new frame was generated
            if generated_frame_path:
                # Analyse Frame
                detections = self.analyse_frame(generated_frame_path)
                
                # Add detections to video object
                for d in detections:
                    # If not already in detections add
                    if d not in self.detections :
                        self.detections.append(d)

                # If person found
                if "person" in self.detections:
                    print("Found a person!")

            #         generateGif(video, cam, currentframe)

                    self.move_to_folder(self.positive_matches)
                    break

                # increasing counter so that it will 
                # show how many frames are created 
                current_frame_number += 1
            else:
                print("All frames generated.\nNo person was found!")

                self.move_to_folder(self.false_positive_folder)
                break

        # Release all space and windows once done 
        cam.release() 
        cv2.destroyAllWindows()

        # Clean up the temp files
        self.clean_temporary_files()
        
        return self