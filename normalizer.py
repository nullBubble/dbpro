from sklearn import preprocessing
import sys
import pandas as pd

class normalizer():

    # set scaling method given as a switch in the terminal
    def __init__(self, string):
        if (string == "-minmax"):
            self.scaler = preprocessing.MinMaxScaler()
        if( string == "-robust"):
            self.scaler = preprocessing.RobustScaler()
        if( string == "-standard"):
            self.scaler = preprocessing.StandardScaler()

    # scales or normalize all the columns listed below with the scaler that was set first
    # depending on if the keepport switch was given in the terminal we scale or ignore the rows with port names
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

    # these values are from the cleaned dataset with -del switch and these functions are for the 
    # single line normalization or standardization. values are provided from a simple help program that is not included 
    def normalize_minmax(self, dff, keepPortname):
        df = dff
        df.at[ 'SHIPTYPE'] = self.calcMinMax(df.at['SHIPTYPE'], 99, 0)
        df.at[ 'SPEED'] = self.calcMinMax(df.at['SPEED'], 54.4, 0.1)
        df.at[ 'LON'] = self.calcMinMax(df.at['LON'], 36.13732, -5.528025)
        df.at[ 'LAT'] = self.calcMinMax(df.at['LAT'], 44.450144, 31.1526)
        df.at[ 'COURSE'] = self.calcMinMax(df.at['COURSE'], 359, 0)
        df.at[ 'HEADING'] = self.calcMinMax(df.at['HEADING'], 511, 0)
        df.at[ 'TIMESTAMP'] = self.calcMinMax(df.at['TIMESTAMP'], 2486, 0)
        if(not keepPortname):
            df.at[ 'DEPARTURE_PORT_NAME'] = self.calcMinMax(df.at[0,'DEPARTURE_PORT_NAME'], 1151, 345)
        
        return df

    def normalize_standard(self, dff, keepPortname):
        df = dff
        df.at[ 'SHIPTYPE'] = self.calcStd(df.at[0,'SHIPTYPE'], 69.89441, 14.44803)
        df.at[ 'SPEED'] = self.calcStd(df.at[0,'SPEED'], 11.14106, 5.19502)
        df.at[ 'LON'] = self.calcStd(df.at[0,'LON'], 11.85457, 10.53640)
        df.at[ 'LAT'] = self.calcStd(df.at[0,'LAT'], 38.58507, 2.74)
        df.at[ 'COURSE'] = self.calcStd(df.at[0,'COURSE'], 174.614597, 102.65382)
        df.at[ 'HEADING'] = self.calcStd(df.at[0,'HEADING'], 204.10748, 136.73664)
        df.at[ 'TIMESTAMP'] = self.calcStd(df.at[0,'TIMESTAMP'], 700.803322, 432.37567)
        if(not keepPortname):
            df.at[ 'DEPARTURE_PORT_NAME'] = self.calcStd(df.at[0,'DEPARTURE_PORT_NAME'], 643.04063, 186.123137)

        return df

    def normalize_robust(self, dff, keepPortname):
        df = dff
        df.at[ 'SHIPTYPE'] = self.calcRobust(df.at[0,'SHIPTYPE'], 70.0, 10.0)
        df.at[ 'SPEED'] = self.calcRobust(df.at[0,'SPEED'], 11.7, 5.3)
        df.at[ 'LON'] = self.calcRobust(df.at[0,'LON'], 9.887167, 16.55377)
        df.at[ 'LAT'] = self.calcRobust(df.at[0,'LAT'], 38.34277, 4.1488)
        df.at[ 'COURSE'] = self.calcRobust(df.at[0,'COURSE'], 166.0, 187.0)
        df.at[ 'HEADING'] = self.calcRobust(df.at[0,'HEADING'], 199.0, 200.0)
        df.at[ 'TIMESTAMP'] = self.calcRobust(df.at[0,'TIMESTAMP'], 686.0, 739.0)
        if(not keepPortname):
            df.at[ 'DEPARTURE_PORT_NAME'] = self.calcRobust(df.at[0,'DEPARTURE_PORT_NAME'], 646.0, 191.0)

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
