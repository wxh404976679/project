#python insert.py '{"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.idCol":"aa","params.TestSize":"0.3","params.RandomState":"0","params.shuffle":"false"}'

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
    id_cols=obj['params.idCol']

    insert_data=range(0,len(df))
    print('insert data',insert_data)

    print("before insert df_shape",df.shape)
    df[id_cols]=insert_data
    print("after insert df_shape",df.shape)

    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir",output_dir)

    df.to_pickle(output_dir+"/1")
    print('successfully')
