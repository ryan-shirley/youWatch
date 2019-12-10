# Importing all necessary libraries for converting video to frame
import cv2 
import os 

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

tempImagesPath = "./data/temp-images/"
tempImagesOutputPath = "./data/temp-images-output/"

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

# Generate frame from video
def generateFrame(cam, currentframe):
        # reading from frame 
        ret,frame = cam.read() 
    
        if ret: 
            # if video is still left continue creating images 
            name = tempImagesPath + '45.jpg'
    
            # writing the extracted images 
            cv2.imwrite(name, frame) 

            # Log
            print("Frame " + name + " was written.")

            return name
            
        else: 
            return False

# Analyse individual frame
def analyseFrame(frame, detector):
    try: 
        # creating a folder named data 
        if not os.path.exists(tempImagesOutputPath): 
            os.makedirs(tempImagesOutputPath) 

    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of ' + tempImagesOutputPath) 

    input_path = frame

    # Replace original temp path to output temp path
    output_path = input_path.replace(tempImagesPath,tempImagesOutputPath)

    # print("Saving analysed frame to " + tempImagesOutputPath + ".")

    detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)

    # Loop through detections found
    detections = []
    for eachItem in detection:
        detections.append(eachItem["name"])
        # print(eachItem["name"] , " : ", eachItem["percentage_probability"])
    
    return detections

# Analyse video file for person
def analyseVideo(video):

    pathToVideo = inputVideoPath + video.originalFile

    # Read the video from specified path 
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
        generatedFrame = generateFrame(cam, currentframe)

        break

        # Check if frame was found and generated
        if generatedFrame:
            # Add generated frame to video object
            video.originalFrames.append(generatedFrame)

            # Analyse Frame
            detections = analyseFrame(generatedFrame, detector)
            
            # Add detections to video object
            for d in detections:
                # If not already in detections add
                if d not in video.detections :
                    video.detections.append(d)

            # If person found then stop
            if finishAfterPersonFound and "person" in video.detections:
                print("Found a person now im finishing!")
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


analyseVideo(Video("2019-11-18T16-27-35.mp4"))