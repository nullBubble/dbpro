import pandas as pd
import numpy as np
import sys
from math import radians,cos,sin,asin,sqrt,atan2,degrees, floor,radians
from datetime import datetime, timedelta
from ship import ship

class interpolation():

    #x lon y lat
    def __init__(self, df):
        self.df = df

    def harvesine(self,lon1,lat1,lon2,lat2):
        earth_rad = 6371.0088
        #convert to rad
        Lon1, Lat1, Lon2, Lat2 = map(radians, [lon1,lat1,lon2,lat2])
        Lat = Lat2-Lat1
        Lon = Lon2-Lon1
        a = sin(Lat / 2.0) ** 2 + cos(Lat1) * cos(Lat2) * sin(Lon / 2.0) ** 2
        d = 2*earth_rad*asin(sqrt(a))
        return d

    def interpolate(self, df, track, row, timejump, i):
        lon1 = track['LON']
        lat1 = track['LAT']
        lon2 = row['LON']
        lat2 = row['LAT']
        time = track['TIMESTAMP']
        earth_rad = 6371.0088
        time_date = datetime.strptime(time, '%d-%m-%y %H:%M')
        route_len = self.harvesine(lon1,lat1,lon2,lat2)
        bearing = self.bearing(lon1,lat1,lon2,lat2)
        bearing = radians(bearing)
        loop_amount = floor((timejump-4)/3) + 1
        part_len = track['SPEED'] * 1.852 / 60 * 3
        p = part_len
        lon1 = radians(lon1)
        lat1 = radians(lat1)
        for i in range(3, int(timejump), 3):
            print(part_len)
            new_time = time_date + timedelta(minutes=i)
            print(new_time)
            new_lat = asin( sin(lat1)*cos(part_len/earth_rad)+cos(lat1)*sin(part_len/earth_rad)*cos(bearing))
            new_lon = lon1 + atan2( sin(bearing)*sin(part_len/earth_rad)*cos(lat1), cos(part_len/earth_rad)-sin(lat1)*sin(new_lat))

            new_lat = degrees(new_lat)
            new_lat = round(new_lat,6)
            new_lon = degrees(new_lon)
            new_lon = round(new_lon,6)

            print(new_lat)
            print(new_lon)

            print("-----------------")
            part_len = part_len + p

        # return df

    def bearing(self,lon1,lat1,lon2,lat2):
        Lon1, Lat1, Lon2, Lat2 = map(radians, [lon1,lat1,lon2,lat2])
        x = sin(Lon2-Lon1)*cos(Lat2)
        y = cos(Lat1)*sin(Lat2)-sin(Lat1)*cos(Lat2)*cos(Lon2-Lon1)
        b = degrees(atan2(x,y))
        return b
        

    def speedcheck(self, track, row):
        # check ship class what each index is 
        lon1 = track['LON']
        lat1 = track['LAT']
        lon2 = row['LON']
        lat2 = row['LAT']
        #knots to km/min
        converted_speed =row['SPEED']* 1.852 / 60

        t1 = track['TIMESTAMP']
        t1_date = datetime.strptime(t1, '%d-%m-%y %H:%M')
        t = row['TIMESTAMP']
        t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
        tdiff = (t_date-t1_date).seconds/60

        dist = self.harvesine(lon1,lat1,lon2,lat2)

        difference = tdiff*converted_speed - dist
        if(difference < 0.045):
            # valid speed jump
            return None
        else:
            # return last recorded speed to reset
            return track['SPEED']
         
