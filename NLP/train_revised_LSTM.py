# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 19:04:41 2021

@author: ASUS
"""

import pandas as pd
import math
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout


def preprocess_input(train_data, n_future, n_past, to_predict):
    
    train_data = pd.read_excel(train_data)

    
    if to_predict == 'SA_NO3':
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3']]
        
    elif to_predict == 'SA_NH4':
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3','SA NH4']]
        

    elif to_predict == 'SA_PO4':
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO','SA NO3','SA NH4','SA PO4']]

    else:
    
        train = train_data[['GHI','TEMP','PH','EC','TURB','SA DO']]

    
    train = train.apply(lambda x: x.fillna(x.mean()),axis=0)

    scaler = MinMaxScaler()

    train_scaled = scaler.fit_transform(train)


    x_train = []
    y_train = []  


    for i in range(n_past, len(train_scaled) - n_future +1):
        
        x_train.append(train_scaled[i - n_past:i, 0:-1])
        y_train.append(train_scaled[i + n_future - 1:i + n_future, -1])


    x_train, y_train = np.array(x_train), np.array(y_train)

    return x_train, y_train

def build_model(x_train, y_train):

    
    model = tf.keras.Sequential()
    model.add(LSTM(64, activation='relu', input_shape=(x_train.shape[1], x_train.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(32, activation='relu', return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(y_train.shape[1]))

    model.compile(optimizer='adam', loss='mse')
    
    return model

###################################################################################
################### THIS IS THE PART THAT YOU NEED TO ADJUST ######################
###################################################################################
    
if __name__ == '__main__':
    
    n_past = 144
    n_future = 4
    
    '''
    Select one variable to train
    Possible values: 'SA_DO', 'SA_NO3', 'SA_NH4', 'SA_PO4'
    '''
    to_predict = 'SA_NH4'
    
    '''
    Specify the complete path to excel file of training data
    '''
    train_dir = 'training905.xlsx'
    
    '''
    Specify the complete path to save the trained model
    '''
    save_dir = '/models/SA_NH4'
    
    
    
    '''
    Train the model
    '''
    x_train, y_train = preprocess_input(train_dir, n_future, n_past, to_predict)
    model = build_model(x_train, y_train)

    model.fit(x_train, y_train, epochs=8, batch_size=32, validation_split=0.1, verbose=1)
    model.save(save_dir)
