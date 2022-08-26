# python weight_sample.py {"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.ratio":"0.5","params.withReplacement":"True","params.weightCol":"age"}

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

    ratio: str = obj['params.ratio']
    print("ratio", ratio)
    withReplacement: str = obj['params.withReplacement']
    print("withReplacement", withReplacement)
    weightCol: str = obj['params.weightCol']
    print("weightCol", weightCol)
    n = int(df.shape[0] * float(ratio))
    df1 = df.sort_values(by=weightCol).head(n)
    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir", output_dir)

    df_write = pd.DataFrame(data=df1, columns=df1.columns)
    # df_write.to_pickle(output_dir + "/1")
    print(df_write)
    print('successfully')
