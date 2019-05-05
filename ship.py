class ship:
    
    def __init__(self, Id, typ, speed, lon, lat, course, heading, timestamp, dep, row):
        self.Id = Id
        self.typ = typ   
        self.dep = dep
        trackinfo ={'SPEED':speed, 'LON':lon, 'LAT':lat,'COURSE':course,'HEADING':heading, 'TIMESTAMP':timestamp, 'ROW':row}
        self.track = []
        self.track.append(trackinfo)
    
    def updateTrack(self, speed, lon, lat, course, heading, timestamp, row):
        
        trackinfo ={'SPEED':speed, 'LON':lon, 'LAT':lat,'COURSE':course,'HEADING':heading, 'TIMESTAMP':timestamp, 'ROW':row}
        self.track.append(trackinfo)

    def getFirstTimestamp(self):
        return self.track[0]['TIMESTAMP']

    def getLastTrack(self):
        return self.track[-1]
    
    def getTrack(self):
        return self.track

    def getID(self):
        return self.Id

    def getType(self):
        return self.typ
    
    def getDep(self):
        return self.dep
