import pandas as pd
import numpy as np
class preclean():

    
    # check for general empty fields, where timestamp exceeds the arrival calc,
    # where speed is zero, as we define a route as a sequence of messagages
    # where the speed is non zero. places all the indices of the rows that
    # fulfill those requirements that are then skipped in the data cleaner
    # and dropped at the end
    def uselessIndices(self, dff):
        df = dff
        index1 = df[df['TIMESTAMP'] > df['ARRIVAL_CALC']].index
        index2 = df[df['ARRIVAL_PORT_CALC'] != df['ARRIVAL_PORT_CALC']].index
        index3 = df[df['ARRIVAL_CALC'] != df['ARRIVAL_CALC']].index
        index4 = df[df['SPEED'] == 0.0].index
        index5 = np.where(pd.isnull(df))[0]
        index = index1.union(index2.union(index3.union(index4.union(index5))))
        
        return index

    # create dictionary where we can look up names and their corresponding int values calculated below
    def createStringToIntMap(self, dff):
        namelist = {}
        df = dff
        df = df.drop(self.uselessIndices(df))
        uniq_names = pd.unique(df[['DEPARTURE_PORT_NAME', 'ARRIVAL_PORT_CALC']].values.ravel('K'))

        for i in range(len(uniq_names)):
            convert = {uniq_names[i]: self.stringToInt(uniq_names[i])}
            namelist.update(convert)
        return namelist

    # convert port names to integers by adding the position of the letters in the alphabet of that 
    # specific word together
    def stringToInt(self, string):
        summe = 0
        for c in string:
            summe = summe + ord(c)
        return summe
