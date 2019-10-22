class ships:
    def __init__(self):
        self.shiplist = []
        
    # check if we have seen this ship before
    def hasShip(self, Id):
        if(Id in [x.Id for x in self.shiplist]):
            return next(ship for ship in self.shiplist if ship.Id == Id)
        return None

    def addShip(self, ship):
        self.shiplist.append(ship)
