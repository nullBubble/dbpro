import pandas as pd
from datetime import datetime
from ship import ship
import time

start = time.time()

def string_to_int(str):
    summe = 0
    for c in str:
        summe = summe + ord(c)
    return summe

def isInShips(Id):
    if(Id in [x.Id for x in ships]):
        return next(ship for ship in ships if ship.Id == Id)
    return None
        
df = pd.read_csv('debs2018_training_labeled_short.csv')
del df['REPORTED_DRAUGHT']
# check for timestamps that are higher than the arrival time
index1 = df[df['TIMESTAMP'] > df['ARRIVAL_CALC']].index
# check for empty arrival port field
index2 = df[df['ARRIVAL_PORT_CALC'] != df['ARRIVAL_PORT_CALC']].index
# check for empty arrival time calculation
index3 = df[df['ARRIVAL_CALC'] != df['ARRIVAL_CALC']].index
# merge all 3 indices into 1, eliminating doubles which 
# would throw an error if they were to be dropped twice
index = index1.union(index2.union(index3))

ships = []

for i in range(df.shape[0]):
    if(i in index):
        continue
    print(i)

    Id = df.iloc[i]['SHIP_ID']
    typ = df.iloc[i]['SHIPTYPE']
    speed = df.iloc[i]['SPEED']
    lon = df.iloc[i]['LON']
    lat = df.iloc[i]['LAT']
    course = df.iloc[i]['COURSE']
    heading = df.iloc[i]['HEADING']
    timestamp = df.iloc[i]['TIMESTAMP']
    dep = df.iloc[i]['DEPARTURE_PORT_NAME']
    s = isInShips(Id)

    if(s == None):
        
        new_ship = ship(Id, typ, speed, lon, lat, course, heading, timestamp, dep, i)
        ships.append(new_ship)
        arr = df.iloc[i]['ARRIVAL_CALC']  
        arr_date = datetime.strptime(arr, '%d-%m-%y %H:%M') 
        t = df.iloc[i]['TIMESTAMP']
        t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
        timediff = (arr_date-t_date).seconds/60
        df.set_value(i, 'ARRIVAL_CALC', timediff)
        df.set_value(i, 'TIMESTAMP', 0)
        
    else:
        
        t1 = s.getFirstTimestamp()
        t1_date = datetime.strptime(t1, '%d-%m-%y %H:%M')
        t = df.iloc[i]['TIMESTAMP']
        t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
        tdiff = (t_date-t1_date).seconds/60
        df.set_value(i, 'TIMESTAMP', tdiff)
        arr = df.iloc[i]['ARRIVAL_CALC']
        arr_date = datetime.strptime(arr, '%d-%m-%y %H:%M')
        timediff = (arr_date-t_date).seconds/60
        df.set_value(i, 'ARRIVAL_CALC', timediff)
        s.updateTrack(speed, lon, lat, course, heading, timestamp, i)
        
    # converting strings to float. needs tweaking
    dep = df.iloc[i]['DEPARTURE_PORT_NAME']
    arrival = df.iloc[i]['ARRIVAL_PORT_CALC']
    df.set_value(i, 'ARRIVAL_PORT_CALC', string_to_int(arrival))
    df.set_value(i, 'DEPARTURE_PORT_NAME', string_to_int(dep))
    
df = df.drop(index)
df.to_csv('bigtest.csv')
end = time.time()
print(end-start)
