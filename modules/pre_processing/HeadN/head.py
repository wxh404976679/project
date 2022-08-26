#python head.py '{"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.size":"5","params.SelectedCols":["train4_converter_temp"]}'

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
    size=int(obj['params.size'])

    df=df.head(size)

    print("df shape",df.shape)
    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir",output_dir)

    df.to_pickle(output_dir+"/1")
    print('successfully')
