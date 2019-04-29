import pandas as pd

class preclean():

    def __init__(self, df):
        self.df = df

    def dropUselessData(self):

        index1 = self.df[self.df['TIMESTAMP'] > self.df['ARRIVAL_CALC']].index
        # check for empty arrival port field
        index2 = self.df[self.df['ARRIVAL_PORT_CALC'] != self.df['ARRIVAL_PORT_CALC']].index
        # check for empty arrival time calculation
        index3 = self.df[self.df['ARRIVAL_CALC'] != self.df['ARRIVAL_CALC']].index
        index4 = self.df[self.df['SPEED'] == 0.0].index
        # merge all 4 indices into 1, eliminating doubles which 
        # would throw an error if they were to be dropped twice
        index = index1.union(index2.union(index3.union(index4)))
        df_dropped = self.df.drop(index)
        return df_dropped

    def createStringToIntMap(self):
        namelist = {}
        df = self.dropUselessData()
        uniq_names = pd.unique(df[['DEPARTURE_PORT_NAME', 'ARRIVAL_PORT_CALC']].values.ravel('K'))

        for i in range(len(uniq_names)):
            convert = {uniq_names[i]: self.stringToInt(uniq_names[i])}
            namelist.update(convert)
        return namelist

    # convert port names to ints
    def stringToInt(self, str):
        summe = 0
        for c in str:
            summe = summe + ord(c)
        return summe