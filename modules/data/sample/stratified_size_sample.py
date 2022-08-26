# python stratified_size_sample.py {"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.strataSizes":"M:2,F:1","params.withReplacement":"True","params.strataCol":"gender"}

import json
import os
import sys

import pandas as pd
from pandas import DataFrame

if __name__ == '__main__':
    pid = os.getpid()
    print("PID:%s" % pid)

    arg1 = sys.argv[1]
    obj = json.loads(arg1)

    input1_dir = obj['params.input.1.dir']
    print("input1_dir", input1_dir)
    df: DataFrame = pd.read_pickle(input1_dir)

    strataSizes: str = obj['params.strataSizes']
    print("strataSizes", strataSizes)
    withReplacement: str = obj['params.withReplacement']
    print("withReplacement", withReplacement)
    strataCol: str = obj['params.strataCol']
    print("strataCol", strataCol)
    df2 = df.groupby(strataCol)
    tmp_df_list = []
    for i in strataSizes.split(","):
        tuple2 = i.split(":")
        col = tuple2[0]
        size = int(tuple2[1])
        tmp_df_list.append(df2.get_group(col).sample(n=size, replace=withReplacement.lower() == str(True).lower()))
    df1 = pd.concat(tmp_df_list)
    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir", output_dir)

    df_write = pd.DataFrame(data=df1, columns=df1.columns)
    # df_write.to_pickle(output_dir + "/1")
    print(df_write)
    print('successfully')
