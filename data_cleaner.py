import pandas as pd
from datetime import datetime
from ship import ship
from ships import ships
from preclean import preclean
from interpolation import interpolation
import time
import sys

def checkColumns(df):
    cols = {'SHIP_ID', 'SHIPTYPE', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP'}
    cols.update({'DEPARTURE_PORT_NAME','REPORTED_DRAUGHT', 'ARRIVAL_CALC', 'ARRIVAL_PORT_CALC'})
    if cols.issubset(df.columns):
        return True
    return False

def calcTimeDifference(timest2, timest1):
    timest2_date = datetime.strptime(timest2, '%d-%m-%y %H:%M')
    timest1_date = datetime.strptime(timest1, '%d-%m-%y %H:%M')
    timediff = (timest2_date-timest1_date).seconds/60
    return timediff

def clean(pc, ip, dff):
    start = time.time()
    shiplist = ships()
    index = pc.uselessIndices()
    df = dff
    del df['REPORTED_DRAUGHT']
    namelist = pc.createStringToIntMap()
    timetreshold = 5
    speedtreshold = 15

    for i, row in df.iterrows():
        if i in index:
            continue
        print("current row:"+str(i))

        Id = row['SHIP_ID']
        typ = row['SHIPTYPE']
        speed = row['SPEED']
        lon = row['LON']
        lat = row['LAT']
        course = row['COURSE']
        heading = row['HEADING']
        timestamp = row['TIMESTAMP']

        dep = row['DEPARTURE_PORT_NAME']
        arrival = row['ARRIVAL_PORT_CALC']
        df.at[i, 'ARRIVAL_PORT_CALC'] = namelist[arrival]
        df.at[i, 'DEPARTURE_PORT_NAME'] = namelist[dep]

        s = shiplist.hasShip(Id)
        if(s == None):
            # add new ship to a list
            new_ship = ship(Id, typ, speed, lon, lat, course, heading, timestamp, dep, i)
            shiplist.addShip(new_ship)
            # compute the difference from this timestamp in regards to the arrival time
            arr = row['ARRIVAL_CALC']  
            t = row['TIMESTAMP']
            df.at[i, 'ARRIVAL_CALC'] = calcTimeDifference(arr, t)
            # set the first timestamp seen for a ship, so a new route, to 0. following
            # timestamps are relative to this 0 time value
            df.at[i, 'TIMESTAMP'] = 0
            
        else:
            # ship already seen atleast once, update track and timestamps with the help of 
            # a ship object which holds the trackinformation for each single ship object
            t1 = s.getFirstTimestamp()
            t = row['TIMESTAMP']
            df.at[i, 'TIMESTAMP'] = calcTimeDifference(t, t1)
            arr = row['ARRIVAL_CALC']
            df.at[i, 'ARRIVAL_CALC'] = calcTimeDifference(arr, t)

            prev_speed = s.getLastTrack()['SPEED']
            # correct erronous speed
            if(speed-prev_speed > speedtreshold):
                check = ip.speedcheck(s.getLastTrack(), row)
                if(check != None):
                    speed = check
                    df.at[i, 'SPEED'] = check
            # interpolate between 2 timestamps that are atleast 5 mins away
            prev_time = s.getLastTrack()['TIMESTAMP']
            timejump = calcTimeDifference(timestamp, prev_time)
            if(timejump > timetreshold):
                df = ip.interpolate(df, s, row, timejump, namelist, i)
                index = pc.uselessIndices()

            s.updateTrack(speed, lon, lat, course, heading, timestamp, i)
            
    df = df.drop(index)
    df.to_csv('interresult3.csv',index=False)
    end = time.time()
    print("time:"+str(end-start))

if __name__ == "__main__":
    csvfile = sys.argv[1]
    if(csvfile.lower().endswith('.csv')):
        df = pd.read_csv(csvfile)
        if(not checkColumns(df)):
            sys.exit("csv file does not have required columns")
        ip = interpolation(df)
        pc = preclean(df)
        clean(pc, ip, df)
    else:
        sys.exit("command line argument is not a csv file")
# else:
#     # data_cleaner got imported