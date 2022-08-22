#!/usr/bin/env python
# coding: utf-8

# In[14]:


import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
import joblib


# In[3]:


#数据标准化
def get_scaler(X_train):
    scaler = StandardScaler()
    X_scler = scaler.fit_transform(X_train)
    return X_scler


# In[4]:


#方差过滤
def get_VT(X,threshold):
    #进行方差的选择
    clf = VarianceThreshold(threshold)
    x_fsvar = clf.fit_transform(X)
    return x_fsvar


# In[23]:


def get_HI_day(data,data_qy,qy_list,model):
    '''输入处理后的宽表的数据，以及只有牵引的宽表数据,以及模型获得该天的设备健康度的得分
    @data:处理后的特征宽表数据
    @data_qy:牵引特征
    @qy_list:模型训练所用的特征
    @model:训练好的模型
    return：该设备该天的设备健康度得分列表'''
    df_gz = data[data["5279"]==2]
    df_gz["score"] = [0]*len(df_gz)
    probs = get_scaler(data_qy[qy_list])
    data_qy["score"] = probs[:,0]
    df_qy_gz = pd.concat([data_qy[["vtime","score"]],df_gz[["vtime","score"]]],axis=0)
    df_qy_gz.index = [*range(len(df_qy_gz))]
    Score = df_qy_gz["score"].mean()
    return Score 


# In[24]:


def get_HI_month(data,data_qy,qy_list,model):
    '''输入处理后的宽表的数据，以及只有牵引的宽表数据,以及模型获得该月份每一天的设备健康度的得分
    @data:处理后的特征宽表数据
    @data_qy:牵引特征
    @qy_list:模型训练所用的特征
    @model:训练好的模型
    return：该月每一天的设备健康度得分列表'''
    df_gz = data[data["5279"]==2]
    df_gz["score"] = [0]*len(df_gz)
    probs = get_scaler(data_qy[qy_list])
    data_qy["score"] = probs[:,0]
    df_qy_gz = pd.concat([data_qy[["vtime","score"]],df_gz[["vtime","score"]]],axis=0)
    df_qy_gz.index = [*range(len(df_qy_gz))]
    df_qy_gz["day"] = df_qy_gz["vtime"].apply(lambda x:str(x)[0:10])
    #获取一个月中
    days = list(df_qy_gz["day"].value_counts().sort_index().index)
    Score_list = []
    for day in days:
        if len(df_qy_gz[df_qy_gz["day"] == day])<=100 :
            score_day = Score_list[-1]
        else:
            score_day = df_qy_gz[df_qy_gz["day"] == day]["score"].mean()
        #score_day = clf.predict_proba(X_day)[:,0].mean()
        Score_list.append(score_day)
    return Score_list


# In[25]:


if __name__ == '__main__':
    #读取模型
    gmm_o_20210525 = joblib.load("./Model/gmm_o_20210525.pkl")
    data = pd.read_csv("./Df_Train/df_all_featurn_05.csv")
    data_qy = pd.read_csv("./Df_Train/df_all_featurn_05_qy.csv")
    fea_list = ["87","89","38_37_v","42_41_v","40_39_v","722_721_v","88_87_p","87_标准差","87_p斜度","87_p峭度"]
    #df_o = data_qy[fea_o]
    get_HI_month(data,data_qy,fea_list,gmm_o_20210525)

