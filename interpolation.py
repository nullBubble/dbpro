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


    def harvesine(self,lon1,lat1,lon2,lat2):

        #convert to rad
        Lon1, Lat1, Lon2, Lat2 = map(radians, [lon1,lat1,lon2,lat2])
        Lat = Lat2-Lat1
        Lon = Lon2-Lon1
        a = sin(Lat / 2.0) ** 2 + cos(Lat1) * cos(Lat2) * sin(Lon / 2.0) ** 2
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

    def speedcheck(self, track, speed, lon, lat, timestamp):
        # check ship class what each index is 
        # lasttrack = track[-1]
        x1 = track['lon']
        y1 = track['lat']
        x2 = lon
        y2 = lat
        #knots to km/min
        converted_speed =speed* 1.852 / 60

        t1 = track['timestamp']
        t1_date = datetime.strptime(t1, '%d-%m-%y %H:%M')
        t = timestamp
        t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
        tdiff = (t_date-t1_date).seconds/60

        dist = self.harvesine(x1,y1,x2,y2)
        difference = tdiff*converted_speed - dist
        if(difference < 0.045):
            return None
        else:
            # return last recorded speed to reset
            return track['speed']
         
