#python RowColConvert.py '{"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.TargetType":"FLOAT","params.SelectedCols":["train4_converter_temp","train4_converter_output_watertemp"]}'

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

    print("before convert data shape:",df.shape)
    print(df)
    df_convert=pd.DataFrame(df.values.T,columns=df.index,index=df.columns)
    print("after convert data shape:",df_convert.shape)
    print(df_convert)

    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir",output_dir)

    df.to_pickle(output_dir+"/1")
    print('successfully')
