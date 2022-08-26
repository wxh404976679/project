import pandas as pd
import sys
import joblib

if __name__=="__main__":

    # df=pd.read_pickle('./91/1')
    df = pd.read_csv('./6001-4.xls')
    print(df)
    df_data = df.loc[:, ["train4_converter_temp"]]
    std=joblib.load('./91/2')
    fea=std.fit_transform(df_data)
    print(fea)
    # df.to_pickle(sys.argv[2])

