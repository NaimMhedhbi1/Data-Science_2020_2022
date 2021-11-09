# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 20:58:49 2021

@author: ASUS
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import load_model



def predict_data(train_data, test_data, model, n_future, n_past, to_predict, save_dir):
    
    train_data = pd.read_excel(train_data)
    test_data = pd.read_excel(test_data)
    
    if to_predict == 'SA_NO3':
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3']]
        test = test_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3']]

    elif to_predict == 'SA_NH4':
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3','SA NH4']]
        test = test_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3','SA NH4']]

    elif to_predict == 'SA_PO4':
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3','SA NH4','SA PO4']]
        test = test_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3','SA NH4','SA PO4']]

    else:
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO']]
        test = test_data[['GHI','TEMP','PH','EC','TURB','SA DO']]
    
    train = train.apply(lambda x: x.fillna(x.mean()),axis=0)

    scaler = MinMaxScaler()

    train_scaled = scaler.fit_transform(train)
    test_scaled = scaler.transform(test)

   
    x_test = []
    y_test = []

    for i in range(n_past, len(test_scaled) - n_future +1):
        x_test.append(test_scaled[i - n_past:i, 0:-1])
        y_test.append(test_scaled[i + n_future - 1:i + n_future, -1])

    x_test, y_test = np.array(x_test), np.array(y_test)

    test_dates = pd.to_datetime(test_data['datetime'])
    test_dates = test_dates[n_future+n_past-1:]
    
    forecast = model.predict(x_test)
    
    forecast_dates = []
    for time_i in test_dates:
        forecast_dates.append(time_i.date())

    forecast_time = []
    for time_i in test_dates:
        forecast_time.append(time_i.time())

    x_test_noscale = []
    y_test_noscale = [] 

    for i in range(n_past, len(test_scaled) - n_future +1):
        x_test_noscale.append(np.asarray(test)[i - n_past:i, 0:test_scaled.shape[1]])
        y_test_noscale.append(np.asarray(test)[i + n_future - 1:i + n_future, -1])
    
    x_test_noscale, y_test_noscale = np.array(x_test_noscale), np.array(y_test_noscale)
    
    forecast_copies = np.repeat(forecast, x_test_noscale.shape[2], axis=-1)
    
    y_pred = scaler.inverse_transform(forecast_copies)[:,-1]
    
    df_pred = pd.concat([pd.DataFrame(forecast_dates), pd.DataFrame(forecast_time), pd.DataFrame(y_pred), pd.DataFrame(y_test_noscale)], axis=1)
    df_pred.columns = ['date','time','prediction '+str(test.columns[-1]), 'test '+str(test.columns[-1])]
    df_pred.to_csv(save_dir)# Dump CSV
    
###################################################################################
################### THIS IS THE PART THAT YOU NEED TO ADJUST ######################
###################################################################################
    
if __name__ == '__main__':
    
    n_past = 144
    n_future = 4
    
    '''
    Select one variable to predict
    Possible values: 'SA_DO', 'SA_NO3', 'SA_NH4', 'SA_PO4'
    '''
    to_predict = 'SA_NH4' 
    
    
    '''
    Specify the complete path to excel file of training and validation data
    '''
    
    train_dir = 'D:/Upwork/Pred_Emp_Data/training905.xlsx'
    test_dir = 'D:/Upwork/Pred_Emp_Data/validation905.xlsx'
    
    '''
    Specify the complete path to the generated csv file after prediction
    '''
    save_dir = 'D:/Upwork/Pred_Emp_Data/NH_4.csv'
    
    
    '''
    Specify the complete path to the trained model folder
    '''
    model = load_model('D:/Upwork/Pred_Emp_Data/SA_NH4')
    
    '''
    Predict validation data
    '''
    predict_data(train_dir, test_dir, model, n_future, n_past, to_predict, save_dir)