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

    def normalize(self, dff, keepPortname):
        df = dff
        scaler = self.scaler
       
        df['SHIPTYPE'] = scaler.fit_transform(df['SHIPTYPE'].values.astype(float).reshape(-1,1))
        df['SPEED'] = scaler.fit_transform(df['SPEED'].values.astype(float).reshape(-1,1))
        df['LON'] = scaler.fit_transform(df['LON'].values.astype(float).reshape(-1,1))
        df['LAT'] = scaler.fit_transform(df['LAT'].values.astype(float).reshape(-1,1))
        df['COURSE'] = scaler.fit_transform(df['COURSE'].values.astype(float).reshape(-1,1))
        df['HEADING'] = scaler.fit_transform(df['HEADING'].values.astype(float).reshape(-1,1))
        df['TIMESTAMP'] = scaler.fit_transform(df['TIMESTAMP'].values.astype(float).reshape(-1,1))
        if(not keepPortname):
            df['DEPARTURE_PORT_NAME'] = scaler.fit_transform(df['DEPARTURE_PORT_NAME'].values.astype(float).reshape(-1,1))
        df['ARRIVAL_CALC'] = scaler.fit_transform(df['ARRIVAL_CALC'].values.astype(float).reshape(-1,1))
        if(not keepPortname):
            df['ARRIVAL_PORT_CALC'] = scaler.fit_transform(df['ARRIVAL_PORT_CALC'].values.astype(float).reshape(-1,1))

        return df

    # these data from the cleaned dataset with -del and these functions are for the single line normalization/standardization
    def normalize_minmax(self, dff, keepPortname):
        df = dff
        df.ix[0, 'SHIPTYPE'] = self.calcMinMax(df.at[0,'SHIPTYPE'], 99, 0)
        df.ix[0, 'SPEED'] = self.calcMinMax(df.at[0,'SPEED'], 54.4, 0.1)
        df.ix[0, 'LON'] = self.calcMinMax(df.at[0,'LON'], 38.827418, -5.528025)
        df.ix[0, 'LAT'] = self.calcMinMax(df.at[0,'LAT'], 44.450144, 29.611588)
        df.ix[0, 'COURSE'] = self.calcMinMax(df.at[0,'COURSE'], 359, 0)
        df.ix[0, 'HEADING'] = self.calcMinMax(df.at[0,'HEADING'], 511, 0)
        df.ix[0, 'TIMESTAMP'] = self.calcMinMax(df.at[0,'TIMESTAMP'], 2545, 0)
        if(not keepPortname):
            df.ix[0, 'DEPARTURE_PORT_NAME'] = self.calcMinMax(df.at[0,'DEPARTURE_PORT_NAME'], 1151, 345)
        
        return df

    def normalize_standard(self, dff, keepPortname):
        df = dff
        df.ix[0, 'SHIPTYPE'] = self.calcStd(df.at[0,'SHIPTYPE'], 69.27547, 15.4021)
        df.ix[0, 'SPEED'] = self.calcStd(df.at[0,'SPEED'], 10.32861, 5.7465)
        df.ix[0, 'LON'] = self.calcStd(df.at[0,'LON'], 11.61679, 10.581109)
        df.ix[0, 'LAT'] = self.calcStd(df.at[0,'LAT'], 38.60534, 2.80637)
        df.ix[0, 'COURSE'] = self.calcStd(df.at[0,'COURSE'], 174.70967, 103.64085)
        df.ix[0, 'HEADING'] = self.calcStd(df.at[0,'HEADING'], 208.02604, 140.01892)
        df.ix[0, 'TIMESTAMP'] = self.calcStd(df.at[0,'TIMESTAMP'], 715.46203, 438.16584)
        if(not keepPortname):
            df.ix[0, 'DEPARTURE_PORT_NAME'] = self.calcStd(df.at[0,'DEPARTURE_PORT_NAME'], 646.2459, 187.93661)

        return df

    def normalize_robust(self, dff, keepPortname):
        df = dff
        df.ix[0, 'SHIPTYPE'] = self.calcRobust(df.at[0,'SHIPTYPE'], 70.0, 10.0)
        df.ix[0, 'SPEED'] = self.calcRobust(df.at[0,'SPEED'], 11.3, 6.1)
        df.ix[0, 'LON'] = self.calcRobust(df.at[0,'LON'], 9.535745, 15.58715)
        df.ix[0, 'LAT'] = self.calcRobust(df.at[0,'LAT'], 38.40793, 4.252385)
        df.ix[0, 'COURSE'] = self.calcRobust(df.at[0,'COURSE'], 169.0, 188.0)
        df.ix[0, 'HEADING'] = self.calcRobust(df.at[0,'HEADING'], 203.0, 203.0)
        df.ix[0, 'TIMESTAMP'] = self.calcRobust(df.at[0,'TIMESTAMP'], 701.0, 739.0)
        if(not keepPortname):
            df.ix[0, 'DEPARTURE_PORT_NAME'] = self.calcRobust(df.at[0,'DEPARTURE_PORT_NAME'], 647.0, 191.0)

        return df

    def calcMinMax(self, val, maximum, minimum):
        x = (val - minimum)/(maximum-minimum)
        return x

    def calcStd(self, val, mean, stdev):
        x = (val-mean)/stdev 
        return x
    
    def calcRobust(self, val, center, scale):
        x = (val-center)/scale
        return x