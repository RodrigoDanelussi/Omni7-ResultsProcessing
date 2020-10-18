class Column:
    def __init__(self):
        self.frame = -1
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.cameraTime = None
        self.imageName = ''

class Continuous:
    def __init__(self):
        self.frame = -1
        self.sentido = ''
        self.type = ''
        self.subType = ''

class Discrete:
    def __init__(self):
        self.frame = -1
        self.sentido = ''
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.type = ''
        self.subType = ''
        self.complement1 = ''
        self.complement2 = ''
        self.image = ''
        