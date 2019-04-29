class ship:
    
    def __init__(self, Id, typ, speed, lon, lat, course, heading, timestamp, dep, row):
        self.Id = Id
        self.typ = typ   
        self.dep = dep
        trackinfo = [speed, lon, lat, course, heading, timestamp, row]
        self.track = []
        self.track.append(trackinfo)
    
    def updateTrack(self, speed, lon, lat, course, heading, timestamp, row):
        trackinfo = [speed, lon, lat, course, heading, timestamp, row]
        self.track.append(trackinfo)

    def getFirstTimestamp(self):
        return self.track[0][-2]
    
    def getTrack(self):
        return self.track
