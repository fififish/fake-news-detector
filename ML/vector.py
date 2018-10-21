#coding:utf-8
from gensim.models import word2vec
import csv
import re

def vector (strinput):
# 加载模型
    model = word2vec.Word2Vec.load("data/model/word2vec_gensim")

    total_feature = []
    for i in range(300):
        locals()['f'+str(i)]=['f{}'.format(i)]
    #with open('{}.csv'.format(fileinput),'r',encoding='utf-8') as f:
     #   next(f)
      #  f_w = csv.reader(f)
    count = 0
        #for row in f_w:
    rowlist = re.sub(r'\'|\]|\[','',strinput)
    rowlist1 =rowlist.split()
    result = []
    for x in rowlist1:
        try:
                #print(x)
            result.append(model[x])
                #print(model[x])
        except:continue
        #result[0][0]+result[1][0]+result[2][0]
    feature = []
    #if len(result)==0: return 0
        #print(len(result[0]))
    for i in range(len(result[0])):
        s = 0
            #print(len(result))
        for j in range(len(result)):
                #print(result[j][i])
            s = result[j][i] + s
        feature.append(s)
    refer = 0
    for i in range(len(feature)):
        refer =1
        locals()['f'+str(i)].append(feature[i])

    if refer == 1: count = count +1
        #Label.append(row[1])
    #with open('news_verification.csv','w',encoding='gb18030',newline='') as w:
     #   w_t = csv.writer(w)
      #  for i in range(count+1):
       #     row = []
        #    for j in range(300):
         #       row.append(locals()['f'+str(j)][i])
        #row.append(Label[i])
          #  w_t.writerow(row)


    for i in range(count + 1):
        row = []
        for j in range(300):
            row.append(locals()['f'+str(j)][i])
    return row