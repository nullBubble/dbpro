import pandas as pd
import numpy as np
import sys

class delete_sub_500:

    def delete(self, dff):
        # delete entries with less than 500 entries even after interpolating
        df = dff
        df_id = df[['SHIP_ID']]
        df_id_count = df_id['SHIP_ID'].value_counts()
        df_sub_500 = df_id_count[df_id_count < 500]

        indexes_to_drop = []
        for i, row in df.iterrows():
            shipid = row['SHIP_ID']
            if(shipid in df_sub_500):
                indexes_to_drop.append(i)

        df = df.drop(df.index[indexes_to_drop])
        return df
