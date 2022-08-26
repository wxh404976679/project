# python ratio_sample.py {"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.ratio":"0.5","params.withReplacement":"True"}

import json
import os
import sys

import pandas as pd
from pandas import DataFrame


def ratio_sample(params: dict):
    input1_dir = params['params.input.1.dir']
    print("input1_dir", input1_dir)
    df: DataFrame = pd.read_pickle(input1_dir)

    ratio: str = params['params.ratio']
    print("ratio", ratio)
    replace: str = params['params.withReplacement']
    print("withReplacement", replace)
    res: DataFrame = df.sample(frac=float(ratio), replace=replace.lower() == str(True).lower())
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
    ratio_sample(obj)

    print('successfully')
