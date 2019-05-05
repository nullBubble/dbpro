import pandas as pd
import numpy as np
class preclean():

    
    def uselessIndices(self, dff):
        df = dff
        index1 = df[df['TIMESTAMP'] > df['ARRIVAL_CALC']].index
        # check for empty arrival port field
        index2 = df[df['ARRIVAL_PORT_CALC'] != df['ARRIVAL_PORT_CALC']].index
        # check for empty arrival time calculation
        index3 = df[df['ARRIVAL_CALC'] != df['ARRIVAL_CALC']].index
        index4 = df[df['SPEED'] == 0.0].index
        # merge all 5 indices into 1, eliminating doubles which 
        # would throw an error if they were to be dropped twice
        # empty cells
        index5 = np.where(pd.isnull(df))[0]
        index = index1.union(index2.union(index3.union(index4.union(index5))))
        
        return index

    def createStringToIntMap(self, dff):
        # create dictionary where we can look up names and their corresponding int values calculated below
        namelist = {}
        df = dff
        df = df.drop(self.uselessIndices(df))
        uniq_names = pd.unique(df[['DEPARTURE_PORT_NAME', 'ARRIVAL_PORT_CALC']].values.ravel('K'))

        for i in range(len(uniq_names)):
            convert = {uniq_names[i]: self.stringToInt(uniq_names[i])}
            namelist.update(convert)
        return namelist

    # convert port names to ints
    def stringToInt(self, string):
        summe = 0
        for c in string:
            summe = summe + ord(c)
        return summe