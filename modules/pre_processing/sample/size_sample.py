# python size_sample.py {"params.input.1.dir":"./6001.pickle","params.output.dir":"./91","params.size":"2","params.withReplacement":"True","params.selectedCols":"name,age"}

import json
import os
import sys

import pandas as pd
from pandas import DataFrame

from modules.utils.data_type_util import convert_str_to_bool


def size_sample(params: dict):
    input1_dir = params['params.input.1.dir']
    print("input1_dir", input1_dir)
    size: str = params['params.size']
    print("size", size)
    replace: str = params['params.withReplacement']
    print("withReplacement", replace)
    output_dir = params['params.output.dir']
    print("output_dir", output_dir)

    df: DataFrame = pd.read_pickle(input1_dir)
    res: DataFrame = df.sample(n=int(size), replace=convert_str_to_bool(replace))
    os.makedirs(output_dir, exist_ok=True)
    df_write = pd.DataFrame(data=res, columns=res.columns)
    df_write.to_pickle(output_dir + "/1")
    # print(df_write)


if __name__ == '__main__':
    pid = os.getpid()
    print("PID:%s" % pid)

    arg1 = sys.argv[1]
    obj = json.loads(arg1)
    size_sample(obj)

    print('successfully')
