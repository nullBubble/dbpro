import pandas as pd
import numpy as np
import sys
from math import radians,cos,sin,asin,sqrt,atan2,degrees, floor,radians
from datetime import datetime, timedelta
from ship import ship

class interpolation():

    #x lon y lat
    def __init__(self):
        self.to_be_interpolated = []

    def harvesine(self,lon1,lat1,lon2,lat2):
        earth_rad = 6371.0088
        #convert to rad
        Lon1, Lat1, Lon2, Lat2 = map(radians, [lon1,lat1,lon2,lat2])
        Lat = Lat2-Lat1
        Lon = Lon2-Lon1
        a = sin(Lat / 2.0) ** 2 + cos(Lat1) * cos(Lat2) * sin(Lon / 2.0) ** 2
        d = 2*earth_rad*asin(sqrt(a))
        return d

    def interpolate(self, df, ship, row, timejump, namelist, pos):

        earth_rad = 6371.0088
        track = ship.getLastTrack()
        position = pos
        # calculate relative time from last point to start
        # new time calc is relative to this timestamp
        time_at_start = ship.getFirstTimestamp()
        time_at_start_date = datetime.strptime(time_at_start, '%d-%m-%y %H:%M')
        time = track['TIMESTAMP']
        time_date = datetime.strptime(time, '%d-%m-%y %H:%M')
        rel_time = (time_date-time_at_start_date).seconds/60

        lon1 = track['LON']
        lat1 = track['LAT']
        lon2 = row['LON']
        lat2 = row['LAT']
        route_len = self.harvesine(lon1,lat1,lon2,lat2)
        bearing = self.bearing(lon1,lat1,lon2,lat2)
        bearing = radians(bearing)
        # calculate loop interval and distance it covers in that amount
        # based on last speed
        loop_amount = floor((timejump-4)/6) + 1
        part_len = track['SPEED'] * 1.852 / 60 * 6
        p = part_len
        lon1 = radians(lon1)
        lat1 = radians(lat1)
        # interp = []
        for i in range(6, int(timejump), 6):
            # new interpolated positions at 6 min intervals
            new_time = rel_time + i

            # calculate new lon and lat position
            new_lat = asin( sin(lat1)*cos(part_len/earth_rad)+cos(lat1)*sin(part_len/earth_rad)*cos(bearing))
            new_lon = lon1 + atan2( sin(bearing)*sin(part_len/earth_rad)*cos(lat1), cos(part_len/earth_rad)-sin(lat1)*sin(new_lat))

            new_lat = degrees(new_lat)
            new_lon = degrees(new_lon)
            new_lat = round(new_lat,6)
            new_lon = round(new_lon,6)

            # get necessary information for new inserted row
            last_arrival_time = df.at[ship.getLastTrack()['ROW'], 'ARRIVAL_CALC']
            
            new_arrival_calc = last_arrival_time-i
            if(new_arrival_calc < 0):
                break
            arrival_port = df.at[ship.getLastTrack()['ROW'],'ARRIVAL_PORT_CALC']
           
            # create new row and insert it at the correct position
            new_row = [ship.getID(),ship.getType(),track['SPEED'],new_lon,new_lat,track['COURSE'],track['HEADING'],new_time,namelist[ship.getDep()],new_arrival_calc,arrival_port]

            # self.to_be_interpolated.append([position, new_row])

            self.to_be_interpolated.append(new_row)

            # interp.append([position, new_row])
            
            # increment the to-be-travelled distance and update 
            # row index for new interpolated row
            part_len = part_len + p
            position = position + 1
        # self.to_be_interpolated.append(interp)
        # return df
    def execute_interpolate(self, dff):

        df = dff
        # for i in range(len(self.to_be_interpolated)):
        #     print(i)
        #     pos = self.to_be_interpolated[i][0]
        #     row = self.to_be_interpolated[i][1]
        #     df = self.insert_row(df, pos, row)
        # # top_start = 0
        # # top_end = pos
        # # bottom_start = pos
        # # bottom_end = df.shape[0]
        
        # # top_half = [*range(top_start,top_end,1)]
        # # bottom_half = range(bottom_start,bottom_end,1)
        # # bottom_half = [x+len(self.to_be_interpolated) for x in bottom_half]
        # # ind = top_half+bottom_half
        # # df.index = ind

        add_df = pd.DataFrame([x for x in self.to_be_interpolated], columns=['SHIP_ID','SHIPTYPE','SPEED','LON','LAT','COURSE','HEADING','TIMESTAMP','DEPARTURE_PORT_NAME','ARRIVAL_CALC','ARRIVAL_PORT_CALC'])
        print(add_df)
        df = df.append(add_df)

        # self.insert_rows(dff, self.to_be_interpolated)
        return df

    def insert_row(self, df, pos, row):
        # insert new row by splitting, inserting at right position
        # done this way so the new row does not overwrite old data
        top_start = 0
        top_end = pos
        bottom_start = pos
        bottom_end = df.shape[0]
        
        top_half = [*range(top_start,top_end,1)]
        bottom_half = range(bottom_start,bottom_end,1)
        bottom_half = [x+1 for x in bottom_half]

        ind = top_half+bottom_half
        df.index = ind
        df.at[pos] = row
        df = df.sort_index()
        return df

    # def insert_rows(self, df, list):
    #     for i in range(1):
    #         sublist = list[i]
    #         if(len(sublist) == 0 ):
    #             continue
    #         print(i)
    #         top_start = 0
    #         top_end = sublist[0][0]
    #         bottom_start = sublist[0][0]
    #         bottom_end = df.shape[0]
    #         print(top_end)
    #         print(bottom_end)
                
    #         top_half = [*range(top_start,top_end,1)]
    #         bottom_half = range(bottom_start,bottom_end,1)
    #         bottom_half = [x+len(sublist) for x in bottom_half]
    #         print(top_half)
    #         print(len(sublist))
    #         print(bottom_half)
    #         ind = top_half+bottom_half
    #         df.index = ind
    #         for i in range(len(sublist)):
    #             df.at[sublist[i][0]] = sublist[i][1]
    #         df = df.sort_index()

    def bearing(self,lon1,lat1,lon2,lat2):
        # calculate bearing cause that information provided by the 
        # ais data is inconsisent
        Lon1, Lat1, Lon2, Lat2 = map(radians, [lon1,lat1,lon2,lat2])
        x = sin(Lon2-Lon1)*cos(Lat2)
        y = cos(Lat1)*sin(Lat2)-sin(Lat1)*cos(Lat2)*cos(Lon2-Lon1)
        b = degrees(atan2(x,y))
        return b
        

    def speedcheck(self, track, row):
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
         
