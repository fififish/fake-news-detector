#coding:utf-8
from sklearn import svm
import numpy as np
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn import datasets,linear_model,metrics
from sklearn.model_selection import train_test_split,cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report

def result (filename):
#print(data.columns.tolist())   #前五行
#print(data.shape)
    data_test = pd.read_csv('{}.csv'.format(filename))
    data = pd.read_csv('politifact_feature_prep.csv')
#print(data.columns.tolist())   #前五行
#print(data.shape)
    title = data.columns.tolist()
    X_title = []
    for i in range(1,len(title)-1):
        X_title.append(title[i])
    X= data[X_title]
    Y =data[[title[len(title)-1]]]

    X_test2 = data_test[X_title]
#print(X_test2)

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0, random_state=0) #如何按照一定的规则对数据进行划分，如30%-TEST
    #print(X_train.shape,Y_test.shape)

    model = svm.SVC(probability=True,kernel='linear')  # kernel = 'linear'
    model.fit(X_train,Y_train.values.ravel())
    for ele in model.predict_proba(X_test2)[0]:
        print(ele)
        max = 0
        if ele>max: max = ele

    return ((model.predict(X_test2)[0]),max)

    #Y_pred = model.predict(X_test)
    #print(accuracy_score(Y_test, Y_pred))

    #target_names = ['FALSE', 'TRUE']
    #print(classification_report(Y_test, Y_pred, target_names=target_names))

#predicted = cross_val_predict(model,X,Y.values.ravel(),cv=10) #10折交叉算法
#print(len(predicted))