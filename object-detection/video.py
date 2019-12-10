class Video:
    # Locations
    tempImagesPath = "./data/temp-images/"
    tempImagesOutputPath = "./data/temp-images-output/"

    def __init__(self, originalFile):
        self.originalFile = originalFile
        self.originalFrames = []
        self.personFound = False
        self.detections = []
        self.fps = 15
        self.framesForGif = []

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

    # Convert the images into animated gif
    def convertImagesToGif()
        images = []
        for filename in self.framesForGif:
            images.append(imageio.imread(filename))

        imageio.mimsave('./data/cctv-animated.gif', images)