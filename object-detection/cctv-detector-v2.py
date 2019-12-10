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

# Locations
inputVideoPath = "./data/input-video/"
personFoundPath = "./data/person-found/"
personNotFoundPath = "./data/person-not-found/"
noDetectionsPath = "./data/no-detections/"

tempImagesPath = "./data/temp-images/"
tempImagesOutputPath = "./data/temp-images-output/"

analysedVideosPath = "./data/analysed-videos/"

model_path = "./models/yolo.h5"

# Settings
outputAnalysedVideo = True

# Generate frame from video
def generateFrame(cam, currentframe):
        # reading from frame 
        ret,frame = cam.read() 
    
        if ret: 
            # if video is still left continue creating images 
            name = tempImagesPath + 'frame' + str(currentframe) + '.jpg'
    
            # writing the extracted images 
            cv2.imwrite(name, frame) 

            # Log
            print("Frame " + name + " was written.")

            return name
            
        else: 
            return False

# Move file to new folder
def moveToFolder(fileToMove, fromPath, toPath):
    # Check person folder exists
    try: 
        # creating a folder 
        if not os.path.exists(toPath): 
            os.makedirs(toPath) 
            print ('Creating directory of ' + toPath) 
    
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of ' + toPath) 

    # Move original file to person found folder
    os.rename(fromPath + fileToMove, toPath + fileToMove)
    return toPath + fileToMove

# Convert frames to video file
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]
 
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
 
    for i in range(len(files)):
        filename=pathIn + files[i]
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        # print(filename)
        #inserting the frames into an image array
        frame_array.append(img)
 
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
 
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()

# Output an analsed video
def outputVideo(video):
    pathIn= tempImagesOutputPath
    pathOut = analysedVideosPath + video.originalFile

    # Need to get original FPS here
    fps = 5.0

    convert_frames_to_video(pathIn, pathOut, fps)

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

    print("Saving analysed frame to " + tempImagesOutputPath + ".")

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

    # Set object detection model
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()
    
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

            # increasing counter so that it will 
            # show how many frames are created 
            currentframe += 1
        else:
            break

    # Release all space and windows once done 
    cam.release() 
    cv2.destroyAllWindows() 

    # Check for detections
    if video.detections:
        # Check if person was found
        if "person" in video.detections:
            moveToFolder(video.originalFile, inputVideoPath, personFoundPath)
        else:
            print("No person was found in detections.")
            moveToFolder(video.originalFile, inputVideoPath, personNotFoundPath)
    else:
        print("No detections were found")
        moveToFolder(video.originalFile, inputVideoPath, noDetectionsPath)

    # Output video file if setting is true
    if outputAnalysedVideo:
        outputVideo(video)

    # Clean up the temp files
    cleanTemporaryFiles()

 
# Get all video files in input folder
files = os.listdir(inputVideoPath)
video_files = [i for i in files if i.endswith('.mp4')]

# Loop over videos in input folder
for video in video_files:
    # Start analysing
    analyseVideo(Video(video))
    # print(video)


# Hard Coded video file analyse
# video = Video("cctv-car-people.mp4")
# analyseVideo(video)
# print(video.detections)

# # Convert video in frames
# frames = getFrameFromVideo(video)

# # Analyse frames and save as images
# analyseFrame(frames)

# # Convert analysed frames back to video file
# imagesToVideo()