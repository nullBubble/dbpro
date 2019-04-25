from datetime import datetime
from vesselobject import vessel

with open("debs2018_training_labeled_short.csv", "r") as f:
    output = f.readlines()

output = [line.split(",") for line in output]
ships = []


def isInShips(Id):
    if(Id in [x.Id for x in ships]):
        return next(ship for ship in ships if ship.Id == Id)
    return None
        

for i in range(1,30):
    Id = output[i][0]
    typ = output[i][1]
    speed = output[i][2]
    lon = output[i][3]
    lat = output[i][4]
    course = output[i][5]
    heading = output[i][6]
    tstamp = output[i][7]
    timestamp = datetime.strptime(tstamp, '%d-%m-%y %H:%M');

    s = isInShips(Id)
    if(s != None):
        s.updateTrack(course, speed, lon, lat, timestamp)
    else:
        ship = vessel(Id, typ, speed, lon, lat, course, heading, timestamp)
        ships.append(ship)

# print(len(ships))
for ship in ships:
    for t in ship.track:
        print(t)