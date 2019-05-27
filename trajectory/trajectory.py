import pandas as pd
import numpy as np
import random

class trajectory():

    def __init__(self, n, csv):
        self.trajectories = []
        self.ids = []
        self.already = []
        df = pd.read_csv(csv)

        index = df[df['ARRIVAL_CALC'] == 0.0].index
        to_be_deleted = []
        for i in range(len(index)-1,0,-1):
            if(index[i-1] == index[i]-1):
                to_be_deleted.append(index[i-1])
        index = [x for x in index if x not in to_be_deleted]
        index = [0] + index
        print(index)
        quit()
        
        # list of indices where a new trajectory starts
        index = df.ne(df.shift()).apply(lambda x: x.index[x].tolist())['SHIP_ID']
        print(n)
        for x in range(n):
            rndm = random.randint(0,df.shape[0]+1)
            
            # tries to get the left number in the sorted indices array if the random number were to be inserted
            # which should be startindex of the trajectory it falls in
            pos = np.searchsorted(index, rndm) - 1

            # reroll pos until new trajectory is found, e.g indexnumber of trajectory not already found in self.already
            while(index[pos] in self.already):
                rndm = random.randint(0,df.shape[0]+1)
                pos = np.searchsorted(index, rndm) - 1

            # if last trajectory is selected
            if(index[pos] == index[-1]):
                # get from start index of last trajectory until last line of dataframe
                traj = df.iloc[index[pos]:df.shape[0]-1]
            else:
                # business as usual
                traj = df.iloc[index[pos]:index[pos+1]]

            self.trajectories.append(traj)
            self.ids.append(traj['SHIP_ID'].unique()[0])
            self.already.append(index[pos])
            

    def getNextTraj(self):
        if( not self.trajectories):
            return
        del self.ids[0]
        return self.trajectories.pop(0)
        

    def getAvailableTrajectories(self):
        return self.ids