#!/usr/bin/env python
# coding: utf-8

# In[1]:


# -*- coding:utf-8 -*-
#特征包括:原始特征，时频域特征，相关性特征


# In[20]:


import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm._tqdm_notebook import tqdm_notebook as tqdm
import seaborn as sns
from datetime import datetime as dt

from feature_extraction import feature_core
# get_ipython().run_line_magic('matplotlib', 'inline')


import warnings 
warnings.filterwarnings('ignore')


# In[4]:


pd.set_option('display.max_columns', None)
plt.rcParams['figure.facecolor'] = 'w'


# In[5]:


#数值型变量
num_list = [37,38,39,40,41,42,43,47,86,87,88,89,90,91,92,93,94,719,720,721,722,727,728,4487,4488,5292,5298,5304,5454,5634]
#分类型变量
cate_list = [15,16,17,18,53,56,335,336,337,338,339,340,341,342,343,344,345,346,347,348,350,351,354,358,359,360,361,362,364,366,367,
    368,369,370,371,372,374,375,376,377,378,379,380,381,382,383,384,387,388,389,390,391,392,393,394,395,396,397,
    5191,5205,5211,5217,5223,5223,5229,5235,5241,5247,5253,5259,5279,5285,5310,5310]
#获得只有0，1表示有故障的变量，将表征状态变量的数据剔除
cate_01_list = [15,16,17,18,53,335,336,337,338,339,340,341,342,343,344,345,346,347,348,350,351,354,358,359,360,361,362,364,366,367,
    368,369,370,371,372,374,375,376,377,378,379,380,381,382,383,384,387,388,389,390,391,392,393,394,395,396,397,
    5191,5205,5211,5217,5223,5223,5229,5235,5241,5247,5253,5259,5310,5310]
#cate_02_list_str = ["15","16","17","18"]
cate_01_list_str = [str(x) for x in cate_01_list]


# In[6]:


def get_qy_data(path,car_num,st_date,end_date):
    '''输入文件所在路径，车辆编号，开始日期，结束日期
    @path：文件所在路径
    @car_num : 车辆的编号
    @st_date:所取文件开始日期
    @end_date:索取文件结束日期
    return：返回要取所有车辆所在日期内的牵引状态的数据'''
    
    file_list = os.listdir(path)
    #print(file_list)
    file_select = [i for i in file_list[1:] if end_date>=int(i[4:12])>=st_date]
    #file_select = [i[4:12] for i in file_list[1:]]
    #print(file_select)
    df_car_num_qy = pd.DataFrame() 
    for day in tqdm(file_select):
        path_pkl = path+day
        print(path_pkl)
        data = pd.read_pickle(path_pkl)
        data_qy = data[(data.train_id == car_num)&(data[5279]==3)]
        df_car_num_qy = pd.concat([df_car_num_qy,data_qy],axis=0)
        df_car_num_qy.index = [*range(len(df_car_num_qy))]
    return df_car_num_qy


# In[19]:


def get_all_data(path,car_num,st_date,end_date):
    '''输入文件所在路径，车辆编号，开始日期，结束日期
    @path：文件所在路径
    @car_num : 车辆的编号
    @st_date:所取文件开始日期
    @end_date:索取文件结束日期
    return：返回要取所有车辆所在日期内的牵引状态的数据'''
    
    file_list = os.listdir(path)
    #print(file_list)
    file_select = [i for i in file_list[1:] if end_date>=int(i[4:12])>=st_date]
    #file_select = [i[4:12] for i in file_list[1:]]
    #print(file_select)
    df_car_num_qy = pd.DataFrame() 
    for day in tqdm(file_select):
        path_pkl = path+day
        print(path_pkl)
        data = pd.read_pickle(path_pkl)
        data_qy = data[(data.train_id == car_num)]
        df_car_num_qy = pd.concat([df_car_num_qy,data_qy],axis=0)
        df_car_num_qy.index = [*range(len(df_car_num_qy))]
    return df_car_num_qy


# In[7]:


#切分时间片段，将超多少的时间片段作为不同标记为不同的时刻
def Get_Part_Traval(df,threshold=1800):
    '''输入数据框，标记该数据框的形式片段
    df:具有vtime变量的数据框
    threshold:划分形式片段的阈值，此处的阈值默认为30分钟
    return：增加变量行驶片段'''

    #df.index = [*range(len(df))]
    time_diff_list = df['vtime'].diff().dt.seconds.tolist()
    #初始化形式片段
    df["Traval_Part"] = [0]*len(df)
    count = 0
    for i in tqdm(range(len(df))):
        try:
            #df["Traval_Part"][i] = count
            #如果前后时间差超过30分钟，则定义为一个新的行驶片段
            if time_diff_list[i] >= threshold:
                count += 1
            df["Traval_Part"][i] = count
            #如果前后的时间差<0,将该事件片段定义为-1
            if time_diff_list[i] < 0:
                df["Traval_Part"][i] = -1
        except:
            ptint("发生错误")
    return df


# #### 提取变量的频域特征

# In[15]:


def get_fea_time_fft(fea_list,df,window=10,step=1):
    '''获取表格中原始输入特征的时频域信息
    @fea_list:输入要提取时频域信息的列表的名称
    @df:输入原始的数据表
    @window:获取提取时频域的时间窗口
    @step:输入提取时频域的步长
    @return:包含时频域特征的数据框'''
    
    Traval_Part_list = list(set(df["Traval_Part"].values.tolist()))
    #利用字典存储df_fsp的信息
    df_fsp = pd.DataFrame()
    for tp in tqdm(Traval_Part_list):
        df_fsp_tp = pd.DataFrame()
        for fsp in tqdm(feature_sp_list):
            data = df[(df["Traval_Part"] == tp)]
            array = data[fsp].values.reshape(len(data),1)
            try:
                array_f = feature_core.sequence_feature(array,window, step)
                df_f = pd.DataFrame(array_f)
                df_f.columns = [f"{fsp}_均值",f"{fsp}_方差",f"{fsp}_标准差",f"{fsp}_众数",f"{fsp}_最大值",f"{fsp}_最小值",                               f"{fsp}_过零点个数",f"{fsp}_极差",f"{fsp}_直流分量",f"{fsp}_p均值",f"{fsp}_p方差",f"{fsp}_p标准差",                               f"{fsp}_p斜度",f"{fsp}_p峭度",f"{fsp}_f均值",f"{fsp}_f方差",f"{fsp}_f标准差",f"{fsp}_f斜度",f"{fsp}_f峭度"]
                df_fsp_tp = pd.concat([df_fsp_tp,df_f],axis=1)
            except:
                pass
        #将所有的时频域特征拼接到一起
        df_fsp = pd.concat([df_fsp,df_fsp_tp],axis=0)
    
    return df_fsp


# #### 提取相关性特征

# In[27]:


def get_coff(x,y):
    '''输入序列获得，x与y序列之间的相关系数'''
    return np.corrcoef(x,y)[0,1]

def fea_coff(seq_x,seq_y, win_size, step_size):
    '''
    Get features of a sequence, with or without window
    :param seq: shape of the sequence: (n,1)
    :param win_size: window size, if window_size == 0, get features without window
    :param step_size: step size
    :return: 2D feature matrix
    '''
    if win_size == 0:
        return get_coff(seq_x,seq_y)
    window_size = win_size
    step_size = step_size
    r = len(seq_x)
    feature_mat = list()

    j = 0
    while j < r - step_size:
        window_x = seq_x[j:j + window_size]
        window_y = seq_y[j:j + window_size]
        win_feature = get_coff(window_x,window_y)
        feature_mat.append(win_feature)
        j += step_size
    return feature_mat


# In[21]:


def get_Difference_fea(df):
    '''输入原始数据，获得该原始数据框添加差值特征的新数据框'''
    df["38_37_v"] = df["38"]-df["37"]
    df["40_39_v"] = df["40"]-df["39"]
    df["42_41_v"] = df["42"]-df["41"]
    df["722_721_v"] = df["722"]-df["721"]
    df["720_719_w"] = df["720"]-df["719"]
    df["5298_86_p"] = df["5298"]-df["86"]
    df["88_87_p"] = df["88"]-df["87"]
    return df


# In[32]:


def get_coff_fea(fea_list,df,window=10,step=1):
    '''输入需要做相关系数两两特征列表
    @fea_list:需要做相关系数的两两特征列表
    @df:原始数据框
    @window:时间窗口
    @step:步长
    '''
    Traval_Part_list = list(set(df["Traval_Part"].values.tolist()))
    df_coff = pd.DataFrame()
    for tp in tqdm(Traval_Part_list):
        df_coff_tp = pd.DataFrame()
        data = df[(df["Traval_Part"] == tp)]
        for fea in fea_list:
            df_coff_tp["{}_coff".format(fea)] = fea_coff(df[fea[0]],df[fea[1]], 10, 1)
        
        df_coff = pd.concat([df_coff,df_coff_tp],axis=0)
        
    return df_coff

