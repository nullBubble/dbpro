import pandas as pd
import numpy as np
import sys

df = pd.read_csv(sys.argv[1])

df_id = df[['SHIP_ID']]
df_id_count = df_id['SHIP_ID'].value_counts()
df_sub_500 = df_id_count[df_id_count < 500]

indexes_to_drop = []
for i, row in df.iterrows():
    print(i)
    shipid = row['SHIP_ID']
    if(shipid in df_sub_500):
        indexes_to_drop.append(i)

df = df.drop(df.index[indexes_to_drop])
df.to_csv('interresultbig_removed.csv',index=False)
   
# class delete_sub_500():

#     def __init__(self, df):
#             self.df = df
    
#     def delete(self):
#             df_id = self.df[['SHIP_ID']]
#             df_id_count = df_id['SHIP_ID'].value_counts()
#             df_sub_500 = df_id_count[df_id_count < 500]

#             indexes_to_drop = []
#             for i, row in self.df.iterrows():
#                 shipid = row['SHIP_ID']
#                 if(shipid in df_sub_500):
#                     indexes_to_drop.append(i)

#             df = self.df.drop(self.df.index[indexes_to_drop])
#             return df