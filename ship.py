class ship:
    
    def __init__(self, Id, typ, speed, lon, lat, course, heading, timestamp, dep, row):
        self.Id = Id
        self.typ = typ   
        self.dep = dep
        trackinfo ={'speed':speed, 'lon':lon, 'lat':lat,'course':course,'heading':heading, 'timestamp':timestamp, 'row':row}
        # trackinfo = [speed, lon, lat, course, heading, timestamp, row]
        self.track = []
        self.track.append(trackinfo)
    
    def updateTrack(self, speed, lon, lat, course, heading, timestamp, row):
        
        trackinfo ={'speed':speed, 'lon':lon, 'lat':lat,'course':course,'heading':heading, 'timestamp':timestamp, 'row':row}
        # trackinfo = [speed, lon, lat, course, heading, timestamp, row]
        self.track.append(trackinfo)

    def getFirstTimestamp(self):
        return self.track[0]['timestamp']

    def getLastTrack(self):
        return self.track[-1]
    
    def getTrack(self):
        return self.track
