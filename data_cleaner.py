import pandas as pd
from datetime import datetime
from ship import ship
from ships import ships
from preclean import preclean
from interpolation import interpolation
from delete_sub_500 import delete_sub_500
from normalizer import normalizer
import time
import sys

# method to prepare a single row
def prepare(row, keepPortname = True):

    speedtreshold = 15
     # delete reported draught
    row = row.drop(columns=['REPORTED_DRAUGHT'])
    Id = row.at['SHIP_ID']
    typ = row.at['SHIPTYPE']
    speed = row.at['SPEED']
    lon = row.at['LON']
    lat = row.at['LAT']
    course = row.at['COURSE']
    heading = row.at['HEADING']
    timestamp = row.at['TIMESTAMP']
    dep = row.at['DEPARTURE_PORT_NAME']
    s = ship_list.hasShip(Id)

    if(s == None):
        # add new ship to a list
        s = ship(Id, typ, speed, lon, lat, course, heading, timestamp, dep, ind)
        ship_list.addShip(s)
        row.at['TIMESTAMP'] = 0
    else:
        # ship already seen atleast once, update track and timestamps with the help of 
        # a ship object which holds the trackinformation for each single ship object
        t1 = s.getFirstTimestamp()
        t = row.at['TIMESTAMP']
        row.at['TIMESTAMP'] = calcTimeDifference(t, t1)

        prev_speed = s.getLastTrack()['SPEED']
        # correct erronous speed
        if(speed-prev_speed > speedtreshold):
            check = interp.speedcheck(s.getLastTrack(), row)
            if(check != None):
                speed = check
                row.at['SPEED'] = check
        
        s.updateTrack(speed, lon, lat, course, heading, timestamp, 0)
        
    if(not keepPortname):
        row.at['DEPARTURE_PORT_NAME'] = pre_clean.stringToInt(dep)
    
    row = norma.normalize_minmax(row, keepPortname)
    return row,s

def checkColumns(df):
    # check if columns availble when converting training data set
    cols = {'SHIP_ID', 'SHIPTYPE', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP'}
    cols.update({'DEPARTURE_PORT_NAME','REPORTED_DRAUGHT', 'ARRIVAL_CALC', 'ARRIVAL_PORT_CALC'})
    if cols.issubset(df.columns):
        return True
    return False

def calcTimeDifference(timest2, timest1):
    # calculate time difference between two time stamps in minutes
    timest2_date = datetime.strptime(timest2, '%d-%m-%y %H:%M')
    timest1_date = datetime.strptime(timest1, '%d-%m-%y %H:%M')
    timediff = (timest2_date-timest1_date).seconds/60
    return timediff

def clean(pc, ip, dff, delete, norm, keepPortname):
    # instantiate objects and set tresholds for speed correction and time interp.
    start = time.time()
    shiplist = ships()
    df = dff
    df = df.drop(columns=['REPORTED_DRAUGHT'])
    index = pc.uselessIndices(df)
    namelist = pc.createStringToIntMap(df)
    timetreshold = 25
    speedtreshold = 15

    for i, row in df.iterrows():

        if(i % 10000 == 0): print("current row:"+str(i))
        # skip to be dropped indices for perfomance
        if i in index:
            continue
        
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
        if(not keepPortname):
            df.at[i, 'ARRIVAL_PORT_CALC'] = namelist[arrival]
            df.at[i, 'DEPARTURE_PORT_NAME'] = namelist[dep]

        s = shiplist.hasShip(Id)
        if(s == None):
            # add new ship to a list
            new_ship = ship(Id, typ, speed, lon, lat, course, heading, timestamp, dep, i)
            shiplist.addShip(new_ship)
            # compute the difference from this timestamp in regards to the arrival time
            # and set that value to the new arrival time
            arr = row['ARRIVAL_CALC']  
            t = row['TIMESTAMP']
            df.at[i, 'ARRIVAL_CALC'] = calcTimeDifference(arr, t)
            # set the first timestamp seen for a ship to 0. following
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
            # interpolate between 2 timestamps that are atleast 25 mins away
            prev_time = s.getLastTrack()['TIMESTAMP']
            timejump = calcTimeDifference(timestamp, prev_time)
            if(timejump > timetreshold):
                ip.interpolate(df, s, row, timejump, namelist)

            s.updateTrack(speed, lon, lat, course, heading, timestamp, i)

    # drop the irrelevant rows and add the interpolated rows and
    # depending on the switches given in the terminal delete and normalize
    df = df.drop(index) 
    df = ip.execute_interpolate(df)    
    if( delete != None):
        df = delete.delete(df)
    if( norm != None):
        df = norm.normalize(df, keepPortname)

    df.to_csv(sys.argv[len(sys.argv)-1],index=False)
    end = time.time()
    print("time:"+str(end-start))

if __name__ == "__main__":
    # give name of input file in terminal and depending on switches instantiate objects,
    # also some generic checks if input file not csv file or has not the required columns
    csvfile = sys.argv[1]
    if(csvfile.lower().endswith('.csv')):
        df = pd.read_csv(csvfile)
        delete = None
        norm = None
        keepPortname = False
        switches = ['-minmax', '-robust', '-standard']
        if(not checkColumns(df)):
            sys.exit("csv file does not have required columns")
        # check for command line switches '-del' and the ones in switches are available
        if('-del' in sys.argv):
            delete = delete_sub_500()
        # preserve port names if keepport switch is given
        if('-keepport' in sys.argv):
            keepPortname = True
        if(any(word in sys.argv for word in switches)):
            index = [word in sys.argv for word in switches].index(True)
            switch = switches[index]
            norm = normalizer(switch)
        ip = interpolation()
        pc = preclean()
        clean(pc, ip, df, delete, norm, keepPortname)
    else:
        sys.exit("command line argument is not a csv file")
else:
    ship_list = ships()
    pre_clean = preclean()
    interp = interpolation()
    norma = normalizer('-minmax')
    ind = 0
