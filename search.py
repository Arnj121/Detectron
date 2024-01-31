import time
import pandas as pd
import detector
import os
import numpy as np

def generatePred():
    index=[]
    labels=[]
    imgs=os.listdir('static/JPEGImages')
    for i in range(4001):
        print("{}/{}".format(i,len(imgs)))
        ret = detector.performImgDet("./JPEGImages/{}".format(imgs[i]),write=False)
        labels.append(ret[1])
        index.append(imgs[i])
    df = pd.DataFrame({'file':index,'labels':labels})
    df.to_csv('./predictions.csv',index=False)

def generate_table(uw,files):
    tempdf = pd.DataFrame(np.array([np.array([0] * len(uw))] * len(files)), columns=uw)
    return tempdf

def update_freq(df, terms,lotsofdata):
    print(terms)
    cc=1
    for w in terms:
        print('currently proccessing word (',cc,' / ',len(terms),')', w)
        cc+=1
        for d in range(len(lotsofdata)):
            if lotsofdata[d].count(w)>=1:
                df.loc[d, w] = 1
    return df

def check_dict(query,labels):
    l=[]
    for i in query:
        print(i)
        if i in labels:
            l.append(i)
    return l

def query_tester(query,labels,df,filenames):
    startTime = time.time()
    q = query.strip().lower().split(' ')
    q = check_dict(q,labels)
    if len(q)==0:
        return 0
    dfq = pd.DataFrame(np.array([np.array([0] * len(labels))]), columns=labels)
    for w in q:
        dfq.loc[0, w] = 1
    result = []
    for i in range(len(filenames)):
        s = np.dot(df.iloc[i], dfq.iloc[0])
        result.append(s)
    print(result)
    dic=[]
    for i in range(len(result)):
        if result[i]!=0:
            dic.append((int(result[i]), "http://localhost:3034/static/JPEGImages/{}".format(filenames[i]),filenames[i]))
    dic.sort(reverse=True)
    endtime = time.time()-startTime
    return [endtime,dic]

def initWords():
    df=pd.read_csv('predictions.csv')
    labels = []
    lotsofdata = []
    for i in df['labels']:
        words=[]
        for j in i[1:-1].replace("'","").split(','):
            if len(j)>0:
                words.append(j)
                labels.append(j.strip())
        words = list(set(words))
        words = ' '.join(words)
        lotsofdata.append(words)
    labels = list(set(labels))
    labels.sort()
    filenames = df['file']
    return labels,lotsofdata,filenames

def searchq(q):
     return query_tester(q,labels,df1,filenames)
# df1=generate_table(labels,filenames)
# df1=update_freq(df1,labels,lotsofdata)
# df1.to_csv('./vector.csv',index=False)
df1 = pd.read_csv('./vector.csv')
labels,lotsofdata,filenames=initWords()


