# python ratio_sample.py {"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.ratio":"0.5","params.withReplacement":"True"}

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
    df1: DataFrame = df.sample(frac=float(ratio), replace=withReplacement.lower() == str(True).lower())
    output_dir = obj['params.output.dir']
    os.makedirs(output_dir, exist_ok=True)
    print("output_dir", output_dir)

    df_write = pd.DataFrame(data=df1, columns=df1.columns)
    df_write.to_pickle(output_dir + "/1")
    # print(df_write)
    print('successfully')

# if __name__ == '__main__':
#     arg1 = sys.argv[1]
#     obj = json.loads(arg1)
#     # print(arg1)
#     input1_dir = obj['params.input.1.dir']
#     print("input1_dir", input1_dir)
#     df_write = pd.DataFrame({"name": ["Tom", "Mary", "Jerry", "Mark"],
#                              "age": [18, 22, 19, 31],
#                              "gender": ["M", "F", "M", "M"]})
#     df_write.to_pickle(input1_dir)
