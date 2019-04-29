import pandas as pd
from datetime import datetime
from ship import ship
import time

start = time.time()

# convert port names to ints
def string_to_int(str):
    summe = 0
    for c in str:
        summe = summe + ord(c)
    return summe

def isInShips(Id):
    if(Id in [x.Id for x in ships]):
        return next(ship for ship in ships if ship.Id == Id)
    return None
        
df = pd.read_csv('debs2018_training_labeled.csv')
del df['REPORTED_DRAUGHT']
# check for timestamps that are higher than the arrival time
index1 = df[df['TIMESTAMP'] > df['ARRIVAL_CALC']].index
# check for empty arrival port field
index2 = df[df['ARRIVAL_PORT_CALC'] != df['ARRIVAL_PORT_CALC']].index
# check for empty arrival time calculation
index3 = df[df['ARRIVAL_CALC'] != df['ARRIVAL_CALC']].index

index4 = df[df['SPEED'] == 0.0].index
# merge all 4 indices into 1, eliminating doubles which 
# would throw an error if they were to be dropped twice
index = index1.union(index2.union(index3.union(index4)))

ships = []

for i, row in df.iterrows():
    if(i in index):
        continue
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
    s = isInShips(Id)

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
    df.at[i, 'ARRIVAL_PORT_CALC'] = string_to_int(arrival)
    df.at[i, 'DEPARTURE_PORT_NAME'] = string_to_int(dep)
    
df = df.drop(index)
df.to_csv('bigtest.csv',index=False)
end = time.time()
print(end-start)
