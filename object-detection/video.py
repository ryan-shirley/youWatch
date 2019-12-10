class Video:
    def __init__(self, originalFile):
        self.originalFile = originalFile
        self.originalFrames = []
        self.personFound = False
        self.detections = []
        self.fps = 15