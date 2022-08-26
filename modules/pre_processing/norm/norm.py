#python norm.py '{"params.input.1.dir":"./6001.pickle","params.input.2.dir":"/90/2","params.output.dir":"./91","params.SelectedCols":["train4_converter_temp"],"params.fillvalue":"0","params.strategy":"value"}'

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
    df = pd.read_pickle(input1_dir)

    select_cols=obj['params.selectedcols']
    # select_cols=['train4_converter_output_watertemp','train4_converter_temp']
    print('select_cols',select_cols)
    df_data=df.loc[:,select_cols]
    print("input data shape",df_data.shape)

    std_scaler=StandardScaler()
    features=std_scaler.fit_transform(df_data)
    print("output data shape", features.shape)
    df_write=pd.DataFrame(data=features,columns=select_cols)

    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir",output_dir)

    df_write.to_pickle(output_dir+"/1")
    joblib.dump(std_scaler,output_dir+"/2")
    print('successfully')