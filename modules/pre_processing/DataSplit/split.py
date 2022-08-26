#python split.py '{"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.FeatureCols":["train4_converter_temp"],"params.TargetCols":["train4_converter_temp"],"params.TestSize":"0.3","params.RandomState":"0","params.shuffle":"false"}'

from sklearn.model_selection import train_test_split
import pandas as pd
import sys
import os
import json
import joblib

if __name__=="__main__":
    pid = os.getpid()
    print("PID:%s" % pid)

    arg1 = sys.argv[1]
    obj = json.loads(arg1)

    input1_dir = obj['params.input.1.dir']
    print("input1_dir",input1_dir )
    df = pd.read_pickle(input1_dir)

    feature=obj['params.FeatureCols']
    target=obj['params.TargetCols']
    rd_state=int(obj['params.RandomState'])
    shuffle=bool(obj['params.shuffle'])
    test_size=float(obj['params.TestSize'])

    if rd_state is None:
        rd_state=None

    if shuffle is None:
        shuffle=True

    print("shuffle",shuffle)
    fea_data=df.loc[:,feature]
    print('select feature shape',fea_data.shape)
    target_data=df.loc[:,target]
    print("select target shape",target_data.shape)
    X_train,X_test,y_train,y_test=train_test_split(fea_data,target_data,test_size=test_size,random_state=rd_state,shuffle=shuffle)
    print("x_train shape:", X_train.shape)

    df_Xtrain=pd.DataFrame(data=X_train,columns=feature)
    df_Xtest=pd.DataFrame(data=X_test, columns=feature)
    df_ytrain=pd.DataFrame(data=y_train, columns=feature)
    df_ytest=pd.DataFrame(data=y_test, columns=feature)

    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir",output_dir)

    df_Xtrain.to_pickle(output_dir+"/1_fea_train")
    df_Xtest.to_pickle(output_dir+"/1_fea_test")
    df_ytrain.to_pickle(output_dir+"/1_target_train")
    df_ytest.to_pickle(output_dir+"/1_target_test")
    print('successfully')
