import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
import numpy


df = pd.read_csv('trainingtestv2.csv')
df = df.drop(df.columns[0],axis=1)
del df['SHIP_ID']


trainX = df.drop(columns=['ARRIVAL_CALC'])
trainY = df[['ARRIVAL_CALC']]

model = Sequential()
n_cols = trainX.shape[1]


model.add(Dense(8, activation='relu', input_shape=(n_cols,)))
model.add(Dense(8, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

early_stopping = EarlyStopping(patience=10)
model.fit(trainX, trainY, validation_split=0.2, epochs=100, callbacks=[early_stopping])

te_X =numpy.array([99, 8.0, 14.57422, 35.81719, 72, 6.0, 765, 605])
# test_X = numpy.transpose(te_X)
test_y_predictions = model.predict(te_X)