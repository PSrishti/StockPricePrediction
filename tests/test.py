import numpy as np
import pandas as pd
import os
import sys
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tqdm.notebook import tqdm_notebook
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger
#from tensorflow.keras import optimizers
from keras import optimizers
from tensorflow import keras
from sklearn.metrics import mean_squared_error
import math

current_dir = os.path.abspath(sys.argv[0])
data_path = os.path.join(current_dir,'src', 'data')
models_path = os.path.join(current_dir, 'src', 'models')

tic = 'AMZN'
model = keras.models.load_model(os.path.join(models_path, tic))

y_pred = model.predict(trim_dataset(x_test_t, BATCH_SIZE), batch_size=BATCH_SIZE)
y_pred = y_pred.flatten()
y_test_t = trim_dataset(y_test_t, BATCH_SIZE)
error = mean_squared_error(y_test_t, y_pred)

print("Error is", error, y_pred.shape, y_test_t.shape)
print(y_pred)
print(y_test_t)

y_pred_org = (y_pred * min_max_scaler.data_range_[3]) + min_max_scaler.data_min_[3]
# min_max_scaler.inverse_transform(y_pred)
y_test_t_org = (y_test_t * min_max_scaler.data_range_[3]) + min_max_scaler.data_min_[3]
# min_max_scaler.inverse_transform(y_test_t)
print (len(y_pred_org))
print (len(y_test_t_org))
#print(y_pred_org)
#print(y_test_t_org)

print('Oct 1st stock price for ',tic,y_pred_org[-1])

test = pd.DataFrame(y_pred_org, y_test_t_org).reset_index()
test = test.rename(columns = {'index': 'Pred', 0: 'Test'})
test = test.set_index(df_test[-200:].index)

plt.figure()
# plt.plot(test[['Pred','Test']])
test.plot()
# plt.plot(y_pred_org)
# plt.plot(y_test_t_org)
plt.rcParams["figure.figsize"] = (15,10)
plt.title(tic + ' Prediction vs Real Stock Price')
plt.ylabel('Price')
plt.xlabel('Date')
plt.legend(['Prediction', 'Real'], loc='upper left')
plt.show()
