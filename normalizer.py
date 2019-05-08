from sklearn import preprocessing
import sys
import pandas as pd

class normalizer():

    def __init__(self, string):
        # set scaling method given as a switch in the terminal
        if (string == "-minmax"):
            self.scaler = preprocessing.MinMaxScaler()
        if( string == "-robust"):
            self.scaler = preprocessing.RobustScaler()
        if( string == "-standard"):
            self.scaler = preprocessing.StandardScaler()

    def normalize(self, dff):
        df = dff
        scaler = self.scaler
        df['SHIPTYPE'] = scaler.fit_transform(df['SHIPTYPE'].values.astype(float).reshape(-1,1))
        df['SPEED'] = scaler.fit_transform(df['SPEED'].values.astype(float).reshape(-1,1))
        df['LON'] = scaler.fit_transform(df['LON'].values.astype(float).reshape(-1,1))
        df['LAT'] = scaler.fit_transform(df['LAT'].values.astype(float).reshape(-1,1))
        df['COURSE'] = scaler.fit_transform(df['COURSE'].values.astype(float).reshape(-1,1))
        df['HEADING'] = scaler.fit_transform(df['HEADING'].values.astype(float).reshape(-1,1))
        df['TIMESTAMP'] = scaler.fit_transform(df['TIMESTAMP'].values.astype(float).reshape(-1,1))
        df['DEPARTURE_PORT_NAME'] = scaler.fit_transform(df['DEPARTURE_PORT_NAME'].values.astype(float).reshape(-1,1))
        df['ARRIVAL_CALC'] = scaler.fit_transform(df['ARRIVAL_CALC'].values.astype(float).reshape(-1,1))
        df['ARRIVAL_PORT_CALC'] = scaler.fit_transform(df['ARRIVAL_PORT_CALC'].values.astype(float).reshape(-1,1))

        return df

    def normalize_row(self, dff):
        df = dff
        df.ix[0, 'SHIPTYPE'] = self.calcMinMax(df.at[0,'SHIPTYPE'], 99, 0)
        df.ix[0, 'SPEED'] = self.calcMinMax(df.at[0,'SPEED'], 102.2, 0)
        df.ix[0, 'LON'] = self.calcMinMax(df.at[0,'LON'], 36.13883, -5.528025)
        df.ix[0, 'LAT'] = self.calcMinMax(df.at[0,'LAT'], 44.42255, 31.1526)
        df.ix[0, 'COURSE'] = self.calcMinMax(df.at[0,'COURSE'], 359, 0)
        df.ix[0, 'HEADING'] = self.calcMinMax(df.at[0,'HEADING'], 511, 0)
        df.ix[0, 'TIMESTAMP'] = self.calcMinMax(df.at[0,'TIMESTAMP'], 2545, 0)
        df.ix[0, 'DEPARTURE_PORT_NAME'] = self.calcMinMax(df.at[0,'DEPARTURE_PORT_NAME'], 1151, 345)
        
        return df

    def calcMinMax(self, val, maximum, minimum):
        x = (val - minimum)/(maximum-minimum)
        print(x)
        return x