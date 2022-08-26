#python save_dataset.py '{"params.input.1.dir":"./91/1","params.input.2.dir":"/90/2","params.output.dir":"./91","params.selectedcols":["train4_converter_temp","train4_converter_input_watertemp"],"params.fillvalue":"29","params.strategy":"value"}'

import pandas as pd
import sys
import os
import json
import sklearn.preprocessing as sp

if __name__=="__main__":
    pid = os.getpid()
    print("PID:%s" % pid)

    arg1 = sys.argv[1]
    obj = json.loads(arg1)

    input1_dir = obj['params.input.1.dir']
    print("input1_dir",input1_dir )
    df_write = pd.read_pickle(input1_dir)

    selected_cols=obj['params.selectedcols']
    fill_value=int(obj['params.fillvalue'])
    df_trans=df_write.loc[:,selected_cols]

    print("load data shape:",df_trans)

    bin=sp.Binarizer(threshold=fill_value)
    new_data=bin.transform(df_trans)

    print("after transform data shape",new_data)
    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir",output_dir)

    df_write.to_pickle(output_dir+"/1")
    print('successfully')

    #
    # df_write.to_csv(output_dir+"/save.csv")
    # print('successfully')
