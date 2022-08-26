import pandas as pd
import sys

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1] + '/1.csv', sep='|', header=None, names=sys.argv[2].split("#"))
    df.to_pickle(sys.argv[1] + '/1')
    print('successfully')
