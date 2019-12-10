# Importing all necessary libraries for converting video to frame
import cv2 
import os 

# Import for image to gif conversion and optimisation
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

# Initialize Cloud Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('./youwatch-homecctv-21bf4eac8f29.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

# Locations
inputVideoPath = "./data/input-video/"
personFoundPath = "./data/person-found/"
personNotFoundPath = "./data/person-not-found/"
noDetectionsPath = "./data/no-detections/"
gifOutputPath = "./data/gif-thumbnails/"

tempImagesPath = "./data/temp-images/"
tempImagesOutputPath = "./data/temp-images-output/"

analysedVideosPath = "./data/analysed-videos/"

model_path = "./models/yolo.h5"

# Resize (resolution / resDownScale) & Compression (80 = low | 200 = high)
resDownScale = 4
compression = '200'
secondsAfter = 5 * 2

# Timer
start_time = time.time()

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
        name = tempImagesPath + 'frame' + str(currentframe) + '.jpg'

        # Resize to 720P
        height , width , layers =  frame.shape
        new_h= round(height/resDownScale)
        new_w= round(width/resDownScale)
        resize = cv2.resize(frame, (new_w, new_h))
        # resize = cv2.resize(frame, (1280, 720))
        cv2.imwrite(name, resize) 

        # Log
        # print("Video frame converted to .jpg - Path: " + name)

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

    # print("Saving analysed frame.")

    detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)

    # Loop through detections found
    detections = []
    for eachItem in detection:
        detections.append(eachItem["name"])
        # print(eachItem["name"] , " : ", eachItem["percentage_probability"])
    
    return detections

# Convert the images into animated gif
def convertImagesToGif(frames, name):
    # Check temp folder exists
        try: 
            # creating a folder named data 
            if not os.path.exists(tempImagesPath): 
                os.makedirs(tempImagesPath) 
                print ('Creating directory of ' + tempImagesPath) 
        # if not created then raise error 
        except OSError: 
            print ('Error: Creating directory of ' + tempImagesPath) 

        images = []
        for filename in frames:
            images.append(imageio.imread(filename))

        # Save Gif
        print('Saving gif.')
        gifName = name.replace('mp4', 'gif')
        imageio.mimsave(gifOutputPath + gifName, images)

        # Optimise Gif
        os.system("./gifsicle -O3 --lossy=" + compression + " --colors 256 -o " + gifOutputPath + gifName + " " + gifOutputPath + gifName)

        return 'converted'

# Remove all files in temp folders
def cleanTemporaryFiles():
    # Clean original
    originalfilelist = [ f for f in os.listdir(tempImagesPath) if f.endswith(".jpg") ]
    for f in originalfilelist:
        os.remove(os.path.join(tempImagesPath, f))
    
    # Clean analysed
    analysedfilelist = [ f for f in os.listdir(tempImagesOutputPath) if f.endswith(".jpg") ]
    for f in analysedfilelist:
        os.remove(os.path.join(tempImagesOutputPath, f))

# Analyse video file for person
def analyseVideo(video):
    print('Starting to analyse video for person')

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
        generatedFrame = generateFrame(cam, currentframe)

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

            # If person found
            if finishAfterPersonFound and "person" in video.detections:
                video.framesForGif.append(generatedFrame)
                print("Found a person! Now generating few more frames for gif!")

                for i in range(secondsAfter):
                    
                    # Skip frames - Get one per second
                    for j in range(round(video.fps / 2)):
                        ret,frame = cam.read() 

                    # Generate Frame
                    frame = generateFrame(cam, currentframe)
                    currentframe += 1

                    # Save frame to list to save as gif
                    video.framesForGif.append(frame)

                # Save Images into animated gif
                convertImagesToGif(video.framesForGif, video.originalFile)

                break

            # increasing counter so that it will 
            # show how many frames are created 
            currentframe += 1
        else:
            print("No person was found!")
            break

    # Release all space and windows once done 
    cam.release() 
    cv2.destroyAllWindows() 

    # Clean up the temp files
    cleanTemporaryFiles()

    # Insert doc into firestore
    ts = time.gmtime()
    db.collection(u'detections').add({
        u'camera': u'Camera Name',
        u'time-taken': round(time.time() - start_time) + ' seconds',
        u'timestamp': time.strftime("%B %d, %Y at %I:%M:%S %p GMT", ts)
    })

# Single Analysis of video
analyseVideo(Video("TEST-CCCTV.mp4"))