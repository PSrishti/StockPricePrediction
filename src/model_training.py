import numpy as npimport pandas as pdimport osimport sysfrom datetime import date, timedeltafrom sklearn.preprocessing import MinMaxScalerfrom tqdm.notebook import tqdm_notebookfrom keras.models import Sequential, load_modelfrom keras.layers import Dense, Dropoutfrom keras.layers import LSTMfrom keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, CSVLogger#from tensorflow.keras import optimizersfrom keras import optimizersfrom tensorflow import kerasfrom data_scraping import get_sp500_tickers, download_stock_pricesTIME_STEPS = 60 BATCH_SIZE = 20params = {        "batch_size": 20,  # 20<16<10, 25 was a bust        "epochs": 50,        "lr": 0.00010000,        "time_steps": 60    }    #Function that will convert data into timeseriesdef build_timeseries(mat, y_col_index):    # y_col_index is the index of column that would act as output column    # total number of time-series samples would be len(mat) - TIME_STEPS    dim_0 = mat.shape[0] - TIME_STEPS    dim_1 = mat.shape[1]    x = np.zeros((dim_0, TIME_STEPS, dim_1))    y = np.zeros((dim_0,))    for i in tqdm_notebook(range(dim_0)):        x[i] = mat[i:TIME_STEPS+i]        y[i] = mat[TIME_STEPS+i, y_col_index]    print("length of time-series i/o",x.shape,y.shape)    return x, y#will remove odd samples for matching batch sizesdef trim_dataset(mat, batch_size):    """    trims dataset to a size that's divisible by BATCH_SIZE    """    no_of_rows_drop = mat.shape[0]%batch_size    if(no_of_rows_drop > 0):        return mat[:-no_of_rows_drop]    else:        return matdef create_feature(tic):    data = df[df['tic'] == tic]    print("Training for ", tic)    df_train = data    df_test = data.iloc[960:,:]    train_cols = ["open","high","low","close","volume","day"]    print("Train and Test size", len(df_train), len(df_test))            # scale the feature MinMax, build array    x = df_train.loc[:,train_cols].values    min_max_scaler = MinMaxScaler()    x_train = min_max_scaler.fit_transform(x)    x_test = min_max_scaler.transform(df_test.loc[:,train_cols])            #create variables for LSTM    x_t, y_t = build_timeseries(x_train, 3)    x_t = trim_dataset(x_t, BATCH_SIZE)    y_t = trim_dataset(y_t, BATCH_SIZE)    x_temp, y_temp = build_timeseries(x_test, 3)    x_val, x_test_t = np.split(trim_dataset(x_temp, BATCH_SIZE),2)    y_val, y_test_t = np.split(trim_dataset(y_temp, BATCH_SIZE),2)def model_training():    for tic in selected_tics:        data = df[df['tic'] == tic]        print("Training for ", tic)        df_train = data        df_test = data.iloc[960:,:]        train_cols = ["open","high","low","close","volume","day"]        print("Train and Test size", len(df_train), len(df_test))            # scale the feature MinMax, build array        x = df_train.loc[:,train_cols].values        min_max_scaler = MinMaxScaler()        x_train = min_max_scaler.fit_transform(x)        x_test = min_max_scaler.transform(df_test.loc[:,train_cols])            #create variables for LSTM        x_t, y_t = build_timeseries(x_train, 3)        x_t = trim_dataset(x_t, BATCH_SIZE)        y_t = trim_dataset(y_t, BATCH_SIZE)        x_temp, y_temp = build_timeseries(x_test, 3)        x_val, x_test_t = np.split(trim_dataset(x_temp, BATCH_SIZE),2)        y_val, y_test_t = np.split(trim_dataset(y_temp, BATCH_SIZE),2)            model = Sequential()        model.add(LSTM(units=50, return_sequences=True, batch_input_shape=(BATCH_SIZE, TIME_STEPS, x_t.shape[2])))        model.add(LSTM(units=50))        model.add(Dense(1))            model.compile(loss='mean_squared_error', optimizer='adam')        model.fit(x_t, y_t, epochs=50, batch_size=BATCH_SIZE, verbose=2)        model.save(os.path.join(models_path, tic + '.h5'))def predict_price(tic):    #current_dir = '/Users/srishtipandey/Desktop/StockPricePrediction/src'    #models_path = os.path.join(current_dir, 'models')    models_path = '/app/src/models'    model = load_model(os.path.join(models_path, tic + '.h5'))    start_date = date.today() - timedelta(days=92)    end_date = date.today()    df_test_trial = download_stock_prices([tic], start_date, end_date)    train_cols = ["open","high","low","close","volume","day"]    x = df_test_trial.loc[:,train_cols]    min_max_scaler = MinMaxScaler(feature_range=(0, 1))     x_scaled = min_max_scaler.fit_transform(x)    x_temp, y_temp = build_timeseries(x_scaled, 3)    y_pred = model.predict(x_temp)    y_pred = y_pred[-1]        # invert scaling for forecast    y = x_scaled[-1:,:]    y[:, 3] = y_pred    predicted_price = min_max_scaler.inverse_transform(y)    return predicted_price[0][3].flatten().tolist()if __name__ == "__main__":    current_dir = os.path.abspath(sys.argv[0])    data_path = os.path.join(current_dir, 'data')    models_path = os.path.join(current_dir, 'models')    ticker_list = get_sp500_tickers()    df = pd.read_parquet(os.path.join(data_path, 'StockPriceDataWebScraped.parquet'))    selected_tics = ['ENPH', 'AMD', 'NVDA', 'ETSY', 'TSLA', 'PAYC', 'MTCH', 'GNRC', 'NOW', 'CZR', 'AMZN', 'AAPL']    model_training()