#coding:gb18030
import pandas as pd
import numpy as np
from sklearn.model_selection  import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn import metrics
from sklearn.metrics import classification_report

def result (fileinput):
    #data_test = pd.read_csv('{}.csv'.format(fileinput))
    lst = []
    for i in range(300):
        lst.append('f{}'.format(i))
    inputfile = dict()
    for i in range(300):
        inputfile[lst[i]] = [fileinput[i]]
    data_test = pd.DataFrame(inputfile)
    #print(data_test)
    data = pd.read_csv('politifact_feature_prep.csv')
#print(data.columns.tolist())   #前五行
#print(data.shape)
    title = data.columns.tolist()
    X_title = []
    for i in range(1,len(title)-1):
        X_title.append(title[i])
    #print(X_title)
    X= data[X_title]
    Y =data[[title[len(title)-1]]]

    X_test2 = data_test[X_title]
    #print(type(X_test2))

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0, random_state=0)


    lr = LogisticRegression(C=1000.0, random_state=0)
    lr.fit(X_train, y_train.values.ravel())
    #Y_pred = lr.predict(X_test)
    max = 0
    for ele in lr.predict_proba(X_test2)[0]:
        
        if ele>max: max = ele

    resultr = str(lr.predict(X_test2)[0])+':'+str(max)
    return resultr

#print(accuracy_score(y_test, Y_pred))
#precision_0 = metrics.precision_score(y_test, Y_pred, labels=['FALSE'], average='macro')  # 指定特定分类标签的精确率
#precision_1 = metrics.precision_score(y_test, Y_pred, labels=['1'], average='macro')
#print(precision_0,precision_1)
    target_names = ['FALSE', 'TRUE']
    #print(classification_report(y_test, Y_pred, target_names=target_names))