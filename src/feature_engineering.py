import numpy as np
import pandas as pd
import os
import sys
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt

current_dir = os.path.abspath(sys.argv[0])
data_folder = os.path.join(current_dir, 'data')

#ticker_list = data_scraping.get_sp500_tickers()

df = pd.read_csv('StockPriceDataWebScraped.csv')

df.isna().sum()/len(df)




# =============================================================================
# df1 = pd.read_csv('SentimentScoreData.csv')
# 
# stock_dataf = df.merge(df1,on=['tic','date'], how='left')
# stock_dataf.date = pd.to_datetime(stock_dataf.date)
# stock_dataf = stock_dataf.sort_values('tic')
# new = stock_dataf
# 
# imputer = KNNImputer(n_neighbors=3, weights='uniform', metric='nan_euclidean')
# 
# data = new[new['tic'] == 'AMZN']
# 
# da = data['neg'].values.reshape(-1, 1)
# imputer.fit(da)
# data['neg'] = imputer.transform(da)
# 
# db = data['neu'].values.reshape(-1, 1)
# imputer.fit(db)
# data['neu'] = imputer.transform(db)
# 
# dc = data['pos'].values.reshape(-1, 1)
# imputer.fit(dc)
# data['pos'] = imputer.transform(dc)
# 
# new_df = data
# new_df
# 
# imputer = KNNImputer(n_neighbors=3, weights='uniform', metric='nan_euclidean')
# counter = 1
# for tic in np.setdiff1d(ticker_list,['AMZN']):
#   data = new[new['tic'] == tic]
#   da = data['neg'].values.reshape(-1, 1)
#   imputer.fit(da)
#   data['neg'] = imputer.transform(da)
#   db = data['neu'].values.reshape(-1, 1)
#   imputer.fit(db)
#   data['neu'] = imputer.transform(db)
#   dc = data['pos'].values.reshape(-1, 1)
#   imputer.fit(dc)
#   data['pos'] = imputer.transform(dc)
#   print(counter, new_df.shape, data.shape)
#   counter = counter + 1
#   #print(data)
#   new_df = pd.concat([new_df, data], ignore_index=True)
# print(new_df)
# 
# new_df= new_df.drop(columns = ['neg_x',	'neu_x',	'pos_x'])
# new_df
# 
# #new_df.to_csv('FinalProcessedData.csv')
# new_df = pd.read_csv("/content/FinalProcessedData.csv")
# new_df = new_df.drop(columns = "Unnamed: 0")
# new_df = new_df.set_index('date')
# 
# =============================================================================
