import pandas as pd
import numpy as np
import sys
from math import radians,cos,sin,asin,sqrt
from datetime import datetime
from ship import ship

class interpolation():

    #x lon y lat
    def __init__(self, df):
        self.df = df

    def harvesine(lon1,lat1,lon2,lat2):

        #convert to rad
        lon1, lat1, lon2, lat2 = map(radians, [lon1,lat1,lon2,lat2])
        lat = lat2-lat1
        lon = lon2-lon1
        a = sin(lat / 2.0) ** 2 + cos(lat1) * cos(lat2) * sin(lon / 2.0) ** 2
        d = 2*6371.0088*asin(sqrt(a))
        return d

    # def interpolate():
    # def timecheck():
    #     t1 = df.at[1, 'TIMESTAMP']
    #     t1_date = datetime.strptime(t1, '%d-%m-%y %H:%M')
    #     t = df.at[2, 'TIMESTAMP']
    #     t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
    #     tdiff = (t_date-t1_date).seconds/60
    #     print(tdiff)
    #     if(tdiff > 5):
    #         interpolate(df, lon1, lat1, lon2, lat2, speed)

    def speedcorrect(self, track, speed):
        x1 = track[-2][1]
        y1 = track[-2][2]

        x2 = track[-1][1]
        y2 = track[-1][2]
        print(x1,y1,x2,y2)
        speed =track[-1][0]
        #knots to km/min
        print(speed)
        speed = speed * 1.852 /60
        print(speed)

        t1 = track[-2][3]
        t1_date = datetime.strptime(t1, '%d-%m-%y %H:%M')
        t = track[-1][3]
        t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
        tdiff = (t_date-t1_date).seconds/60
        print(tdiff)

        dist = harvesine(x1,y1,x2,y2)
        print(dist)
        difference = tdiff*speed - dist
        if(difference < 0.045):
            print("seems correct")
        else:
            # TODO: resetting faulty speed
            print("speed seems too high, resetting speed")
        print(difference) # = 0.03
        # treshold 0.05?


    # def check():
    #     treshold = 15
        
    #     # emulate ship object track
    #     track = [[8.2,14.56034,35.8109,'10-03-15 12:15'],[8.1,14.56537,35.81219,'10-03-15 12:17'],[28,14.56962,35.81499,'10-03-15 12:19']]
    #     #
    #     speed1 = track[-2][0]
    #     speed2 = track[-1][0]
    #     if(speed2-speed1>treshold):
    #         speedcorrect(track)
    # check()