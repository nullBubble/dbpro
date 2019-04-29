import pandas as pd
from datetime import datetime
from ship import ship
import time
import sys


def dropUselessData(df):

    index1 = df[df['TIMESTAMP'] > df['ARRIVAL_CALC']].index
    # check for empty arrival port field
    index2 = df[df['ARRIVAL_PORT_CALC'] != df['ARRIVAL_PORT_CALC']].index
    # check for empty arrival time calculation
    index3 = df[df['ARRIVAL_CALC'] != df['ARRIVAL_CALC']].index
    index4 = df[df['SPEED'] == 0.0].index
    # merge all 4 indices into 1, eliminating doubles which 
    # would throw an error if they were to be dropped twice
    index = index1.union(index2.union(index3.union(index4)))
    df_dropped = df.drop(index)
    return df_dropped

def createStringToIntMap(dff):
    namelist = {}
    df = dropUselessData(dff)
    uniq_names = pd.unique(df[['DEPARTURE_PORT_NAME', 'ARRIVAL_PORT_CALC']].values.ravel('K'))

    for i in range(len(uniq_names)):
        convert = {uniq_names[i]: string_to_int(uniq_names[i])}
        namelist.update(convert)
    return namelist

# convert port names to ints
def string_to_int(str):
    summe = 0
    for c in str:
        summe = summe + ord(c)
    return summe

def isInShips(Id, ships):
    if(Id in [x.Id for x in ships]):
        return next(ship for ship in ships if ship.Id == Id)
    return None

def clean(dff, namelist):
    start = time.time()
    ships = []
    df = dropUselessData(dff)
    del df['REPORTED_DRAUGHT']

    for i, row in df.iterrows():
        # if(i in index):
        #     continue
        print(i)

        Id = row['SHIP_ID']
        typ = row['SHIPTYPE']
        speed = row['SPEED']
        lon = row['LON']
        lat = row['LAT']
        course = row['COURSE']
        heading = row['HEADING']
        timestamp = row['TIMESTAMP']
        dep = row['DEPARTURE_PORT_NAME']
        s = isInShips(Id, ships)

        if(s == None):
            # add new ship to a list
            new_ship = ship(Id, typ, speed, lon, lat, course, heading, timestamp, dep, i)
            ships.append(new_ship)
            # compute the difference from this timestamp in regards to the arrival time
            arr = row['ARRIVAL_CALC']  
            arr_date = datetime.strptime(arr, '%d-%m-%y %H:%M') 
            t = row['TIMESTAMP']
            t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
            timediff = (arr_date-t_date).seconds/60
            df.at[i, 'ARRIVAL_CALC'] = timediff
            # set the first timestamp seen for a ship, so a new route, to 0. following
            # timestamps are relative to this 0 time value
            df.at[i, 'TIMESTAMP'] = 0
            
        else:
            # ship already seen atleast once, update track and timestamps with the help of 
            # a ship object which holds the trackinformation for each single ship object
            t1 = s.getFirstTimestamp()
            t1_date = datetime.strptime(t1, '%d-%m-%y %H:%M')
            t = row['TIMESTAMP']
            t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
            tdiff = (t_date-t1_date).seconds/60
            df.at[i, 'TIMESTAMP'] = tdiff
            arr = row['ARRIVAL_CALC']
            arr_date = datetime.strptime(arr, '%d-%m-%y %H:%M')
            timediff = (arr_date-t_date).seconds/60
            df.at[i, 'ARRIVAL_CALC'] = timediff
            s.updateTrack(speed, lon, lat, course, heading, timestamp, i)
            
        # converting strings to int. needs tweaking
        dep = row['DEPARTURE_PORT_NAME']
        arrival = row['ARRIVAL_PORT_CALC']
        df.at[i, 'ARRIVAL_PORT_CALC'] = namelist[arrival]
        df.at[i, 'DEPARTURE_PORT_NAME'] = namelist[dep]
        
    # df = dropUselessData(df)
    df.to_csv('bigtest.csv',index=False)
    end = time.time()
    print(end-start)

if __name__ == "__main__":
    csvfile = sys.argv[1]
    if(csvfile.lower().endswith('.csv')):
        df = pd.read_csv(csvfile)
        namelist = createStringToIntMap(df)
        clean(df, namelist)
    else:
        sys.exit("command line argument is not a csv file")
# else:
#     # data_cleaner got imported