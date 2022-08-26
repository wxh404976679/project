# python stratified_ratio_sample.py {"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.strataRatios":"M:0.5,F:0.5","params.withReplacement":"True","params.strataCol":"gender"}

import json
import os
import sys

import pandas as pd
from pandas import DataFrame


def stratified_ratio_sample(params: dict):
    input1_dir = params['params.input.1.dir']
    print("input1_dir", input1_dir)
    df: DataFrame = pd.read_pickle(input1_dir)

    stratified_ratio: str = params['params.strataRatios']
    print("strataRatios", stratified_ratio)
    replace: str = params['params.withReplacement']
    print("withReplacement", replace)
    stratified_column: str = params['params.strataCol']
    print("strataCol", stratified_column)
    df2 = df.groupby(stratified_column)
    tmp_df_list = []
    for i in stratified_ratio.split(","):
        tuple2 = i.split(":")
        column = tuple2[0]
        ratio = float(tuple2[1])
        tmp_df_list.append(df2.get_group(column).sample(frac=ratio, replace=replace.lower() == str(True).lower()))
    res = pd.concat(tmp_df_list)
    output_dir = params['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir", output_dir)

    df_write = pd.DataFrame(data=res, columns=res.columns)
    df_write.to_pickle(output_dir + "/1")
    # print(df_write)


if __name__ == '__main__':
    pid = os.getpid()
    print("PID:%s" % pid)

    arg1 = sys.argv[1]
    obj = json.loads(arg1)
    stratified_ratio_sample(obj)

    print('successfully')
