#!/usr/bin/env python
# coding: utf-8

# #### 获取原始数据的特征宽表

# In[2]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm._tqdm_notebook import tqdm_notebook as tqdm
import seaborn as sns
from datetime import datetime as dt

from feature_extraction import feature_core
import Get_Feature_Qy
# get_ipython().run_line_magic('matplotlib', 'inline')


import warnings 
warnings.filterwarnings('ignore')


# In[6]:


def get_qyfea_widetable(path,car_num,st_date,end_date,fea_list=[40],window=10,step=1):
    '''输入数据路径，车辆编号，提取时间日期，以及需要提取的时频域的特征列表获取特征宽表
    '''
    data = Get_Feature_Qy.get_qy_data(path,car_num,st_date,end_date)
    data_tp = Get_Feature_Qy.Get_Part_Traval(data)
    Traval_Part_list = list(set(data["Traval_Part"].values.tolist()))
    #相关特征
    data_coff = Get_Feature_Qy.get_Difference_fea(data)
    #时频域特征
    data_tf = Get_Feature_Qy.get_fea_time_fft(fea_list,data_coff)
    
    #将原始的数据框的每一个行驶片段的最后step行删除
    new_data = pd.DataFrame()
    for tp in tqdm(Traval_Part_list):
        data_01 = data_coff[(data_coff["Traval_Part"] == tp)]
        data_01.drop(data_01.iloc[-1:,:].index,inplace = True)
        new_data = pd.concat([new_data,data_01],axis=0)
        
    #将new__data与data_tf拼接
    new_data.index = [*range(len(new_data))]
    data_tf.index = [*range(len(data_tf))]
    #将三个表格拼接在一起形成一个较大的表格
    df_all_featurn_qy = pd.concat([new_data,data_tf],axis=1)
    return df_all_featurn_qy


# In[10]:


def get_fea_widetable(path,car_num,st_date,end_date,fea_list=[40],window=10,step=1):
    '''输入数据路径，车辆编号，提取时间日期，以及需要提取的时频域的特征列表获取特征宽表
    '''
    data = Get_Feature_Qy.get_all_data(path,car_num,st_date,end_date)
    data_tp = Get_Feature_Qy.Get_Part_Traval(data)
    Traval_Part_list = list(set(data["Traval_Part"].values.tolist()))
    #相关特征
    data_coff = Get_Feature_Qy.get_Difference_fea(data)
    #时频域特征
    data_tf = Get_Feature_Qy.get_fea_time_fft(fea_list,data_coff)
    
    #将原始的数据框的每一个行驶片段的最后step行删除
    new_data = pd.DataFrame()
    for tp in tqdm(Traval_Part_list):
        data_01 = data_coff[(data_coff["Traval_Part"] == tp)]
        data_01.drop(data_01.iloc[-1:,:].index,inplace = True)
        new_data = pd.concat([new_data,data_01],axis=0)
        
    #将new__data与data_tf拼接
    new_data.index = [*range(len(new_data))]
    data_tf.index = [*range(len(data_tf))]
    #将三个表格拼接在一起形成一个较大的表格
    df_all_featurn_qy = pd.concat([new_data,data_tf],axis=1)
    return df_all_featurn_qy


# #### 以数据框的形式存入

# In[15]:


#数值型变量
num_list = [37,38,39,40,41,42,43,47,86,87,88,89,90,91,92,93,94,719,720,721,722,727,728,4487,4488,5292,5298,5304,5454,5634]
#分类型变量
cate_list = [15,16,17,18,53,56,335,336,337,338,339,340,341,342,343,344,345,346,347,348,350,351,354,358,359,360,361,362,364,366,367,
    368,369,370,371,372,374,375,376,377,378,379,380,381,382,383,384,387,388,389,390,391,392,393,394,395,396,397,
    5191,5205,5211,5217,5223,5223,5229,5235,5241,5247,5253,5259,5279,5285,5310,5310]
# data以csv或者pkl文件，包含时间变量：vtime,以及包含num_list和cate_list等变量


# In[ ]:


def get_qyfea_widetable_01(data,fea_list=["40","47","87","88","89","90","91","719","721"],window=10,step=1):
    '''数据以data的格式输入，data只包含牵引状态的数据，以及需要提取的时频域的特征列表获取特征宽表
    '''
    #data = Get_Feature_Qy.get_qy_data(path,car_num,st_date,end_date)
    data_tp = Get_Feature_Qy.Get_Part_Traval(data)
    Traval_Part_list = list(set(data["Traval_Part"].values.tolist()))
    #相关特征
    data_coff = Get_Feature_Qy.get_Difference_fea(data)
    #时频域特征
    data_tf = Get_Feature_Qy.get_fea_time_fft(fea_list,data_coff)
    
    #将原始的数据框的每一个行驶片段的最后step行删除
    new_data = pd.DataFrame()
    for tp in tqdm(Traval_Part_list):
        data_01 = data_coff[(data_coff["Traval_Part"] == tp)]
        data_01.drop(data_01.iloc[-1:,:].index,inplace = True)
        new_data = pd.concat([new_data,data_01],axis=0)
        
    #将new__data与data_tf拼接
    new_data.index = [*range(len(new_data))]
    data_tf.index = [*range(len(data_tf))]
    #将三个表格拼接在一起形成一个较大的表格
    df_all_featurn_qy = pd.concat([new_data,data_tf],axis=1)
    return df_all_featurn_qy


# In[ ]:


def get_fea_widetable_01(data,fea_list=["40","47","87","88","89","90","91","719","721"],window=10,step=1):
    '''数据以data的格式输入，data包含状态的数据，以及需要提取的时频域的特征列表获取特征宽表
    '''
    #data = Get_Feature_Qy.get_qy_data(path,car_num,st_date,end_date)
    data_tp = Get_Feature_Qy.Get_Part_Traval(data)
    Traval_Part_list = list(set(data["Traval_Part"].values.tolist()))
    #相关特征
    data_coff = Get_Feature_Qy.get_Difference_fea(data)
    #时频域特征
    data_tf = Get_Feature_Qy.get_fea_time_fft(fea_list,data_coff)
    
    #将原始的数据框的每一个行驶片段的最后step行删除
    new_data = pd.DataFrame()
    for tp in tqdm(Traval_Part_list):
        data_01 = data_coff[(data_coff["Traval_Part"] == tp)]
        data_01.drop(data_01.iloc[-1:,:].index,inplace = True)
        new_data = pd.concat([new_data,data_01],axis=0)
        
    #将new__data与data_tf拼接
    new_data.index = [*range(len(new_data))]
    data_tf.index = [*range(len(data_tf))]
    #将三个表格拼接在一起形成一个较大的表格
    df_all_featurn_qy = pd.concat([new_data,data_tf],axis=1)
    return df_all_featurn_qy


# In[11]:


if __name__ == '__main__':
    path = "/home/crrc/ssd/20201222-nl-data/20201222/test"
    tf = get_fea_widetable(path,"NLCJ_T2",20200201,20200202)

#    get_fea_widetable_01(data,fea_list=["40","47","87","88","89","90","91","719","721"],window=10,step=1)



