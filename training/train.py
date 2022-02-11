# coding=utf-8
import os
import json
import pickle
import pandas as pd
import numpy as np
import sklearn.model_selection
import sklearn.datasets
import sklearn.metrics
from sklearn.metrics import confusion_matrix, recall_score, classification_report, precision_score
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

import autosklearn.regression

data = pd.read_csv('all_data.csv')
print(data.columns)
data = data.drop('Unnamed: 0',axis=1)
print(data.head())


target = data['building_price']
target.columns = ['target']
data = data.drop('building_price',axis=1)
print(type(target))
print(target.shape)


from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(data, target, test_size = 0.2, random_state = 0)
print(type(X_train))
print(type(Y_train))
print(type(X_test))
print(type(Y_test))

print(X_train.head())


automl = autosklearn.regression.AutoSklearnRegressor(
    time_left_for_this_task=120,
    per_run_time_limit=30,
    delete_tmp_folder_after_terminate=False,
    resampling_strategy='cv',
    resampling_strategy_arguments={'folds': 5},
  )
print(X_train)
print(Y_train)


automl.fit(X_train.copy(), Y_train.copy(), dataset_name='digits')

automl.refit(X_train.copy(), Y_train.copy())

print(automl.show_models())


columns = ['postal_code', 'building_shifting_total_area', 'type', 'total_floor',
       'building_state', 'main_use', 'building_materials', 'building_age',
       'building_room_num', 'building_hall_num', 'building_bathroom_num',
       'residential_guard', 'berth', 'elevator']
lst = ["700","100","1","10","4","2","1","100","1","2","3","1","1","1"] 
print(len(columns))
print(len(lst))
df = pd.DataFrame([lst], columns =columns, dtype = int) 


predictions = automl.predict(df)
print(predictions)

print(type(X_test))

predictions = automl.predict(X_test)