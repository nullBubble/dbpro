class vessel:
    
    track = []

    def __init__(self, Id, typ, speed, lon, lat, course, heading, timestamp):
        self.Id = Id
        self.typ = typ    # https://help.marinetraffic.com/hc/en-us/articles/205579997-What-is-the-significance-of-the-AIS-Shiptype-number-
        # self.speed = speed
        # self.lon = lon
        # self.lat = lat
        self.heading = heading # 0-359 degree
        # self.timestamp = timestamp
        # self.course = course # degree relative to north?
        trackinfo = [course, speed, lon, lat, timestamp]
        self.track.append(trackinfo)
    
    def updateTrack(self, course, speed, lon, lat, timestamp):
        trackinfo = [course, speed, lon, lat, timestamp]
        self.track.append(trackinfo)
