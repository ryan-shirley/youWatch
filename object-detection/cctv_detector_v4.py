# Importing all necessary libraries for converting video to frame
import cv2 
import os 

# Import for image to gif conversion
import imageio

# Object detection importing
from imageai.Detection import ObjectDetection

# Image to video conversion
import numpy as np
from os.path import isfile, join

# Custom classes
from video import Video

# Track time for how long to execute
import time

# Locations
inputVideoPath = "./data/input-video/"
personFoundPath = "./data/person-found/"
personNotFoundPath = "./data/person-not-found/"
noDetectionsPath = "./data/no-detections/"

analysedVideosPath = "./data/analysed-videos/"

model_path = "./models/yolo.h5"

start_time = ''

# Settings
finishAfterPersonFound = True

# Set object detection model
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()

# Analyse video file for person
def analyseVideo(video):
    # Read the video from specified path
    pathToVideo = inputVideoPath + video.originalFile 
    cam = cv2.VideoCapture(pathToVideo) 
    
    # Check temp folder exists
    try: 
        # creating a folder named data 
        if not os.path.exists(tempImagesPath): 
            os.makedirs(tempImagesPath) 
            print ('Creating directory of ' + tempImagesPath) 
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of ' + tempImagesPath) 

    # frame details
    currentframe = 0

    # Loop through video file
    while(True): 

        # Send to get indiviudal frame
        generatedFrame = video.generateFrame(cam, currentframe)

        break

        # Check if frame was found and generated
        if generatedFrame:
            # Add generated frame to video object
            video.originalFrames.append(generatedFrame)

            # Analyse Frame
            detections = video.analyseFrame(generatedFrame, detector)
            
            # Add detections to video object
            for d in detections:
                # If not already in detections add
                if d not in video.detections :
                    video.detections.append(d)

            # If person found
            if finishAfterPersonFound and "person" in video.detections:
                video.framesForGif.append(generatedFrame)
                print("Found a person now im generating few more frames for gif!")

                for i in range(5 * video.fps):
                    # Generate Frame
                    frame = video.generateFrame(cam, currentframe)

                    # Save frame to list to save as gif
                    video.framesForGif.append(fame)

                # TODO: Save Images into animated gif
                video.convertImagesToGif()

                break

            # increasing counter so that it will 
            # show how many frames are created 
            currentframe += 1
        else:
            break

    # Release all space and windows once done 
    cam.release() 
    cv2.destroyAllWindows() 

    print("Time taken: %s seconds." % (time.time() - start_time))

# Single Analysis of video
analyseVideo(Video("2019-11-18T16-27-35.mp4"))