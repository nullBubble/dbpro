import pandas as pd
import numpy as np

df = pd.read_csv('bigtest.csv')

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
df.to_csv('bigtest.csv')
   
