#python read_dataset.py '{"params.input.1.dir":"./6001-4.xls","params.input.2.dir":"/90/2","params.output.dir":"./91","params.selectedcols":["train4_converter_temp"],"params.fillvalue":"0","params.strategy":"value"}'

from sklearn.preprocessing import StandardScaler
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
    df_write = pd.read_csv(input1_dir)

    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir",output_dir)

    df_write.to_pickle(output_dir+"/1")
    print('successfully')
