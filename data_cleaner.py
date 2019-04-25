import pandas as pd
from datetime import datetime

def string_to_int(str):
    summe = 0
    for c in str:
        summe = summe + ord(c)
    return summe



df = pd.read_csv('debs2018_training_labeled_short.csv')
# df = df.drop(df.columns[0],axis=1)
# 50% der daten haben ein invaliden heading wert
del df['HEADING']
del df['REPORTED_DRAUGHT']

index = df[df['TIMESTAMP'] > df['ARRIVAL_CALC']].index
shipids = []
timestamps = []

for i in range(df.shape[0]):
    shipid = df.iloc[i]['SHIP_ID']
    if(shipid not in shipids):
        shipids.append(shipid)
        a = df.iloc[i]['ARRIVAL_CALC']
        a_date = datetime.strptime(a, '%d-%m-%y %H:%M')
        t = df.iloc[i]['TIMESTAMP']
        t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
        timediff = (a_date-t_date).seconds/60
        df.set_value(i, 'ARRIVAL_CALC', timediff)
        timestamps.append(df.iloc[i]['TIMESTAMP'])
        df.set_value(i, 'TIMESTAMP', 0)
    else:
        
        t1 = timestamps[-1]
        t1_date = datetime.strptime(t1, '%d-%m-%y %H:%M')
        t = df.iloc[i]['TIMESTAMP']
        t_date = datetime.strptime(t, '%d-%m-%y %H:%M')
        tdiff = (t_date-t1_date).seconds/60
        df.set_value(i, 'TIMESTAMP', tdiff)
        a = df.iloc[i]['ARRIVAL_CALC']
        a_date = datetime.strptime(a, '%d-%m-%y %H:%M')
        timediff = (a_date-t_date).seconds/60
        df.set_value(i, 'ARRIVAL_CALC', timediff)

for i in range(df.shape[0]):
    dep = df.iloc[i]['DEPARTURE_PORT_NAME']
    arr = df.iloc[i]['ARRIVAL_PORT_CALC']
    df.set_value(i, 'ARRIVAL_PORT_CALC', string_to_int(arr))
    df.set_value(i, 'DEPARTURE_PORT_NAME', string_to_int(dep))


# df = df.drop(index)
df.to_csv('trainingtestv2.csv')
