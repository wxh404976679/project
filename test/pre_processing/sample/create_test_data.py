import pandas as pd

if __name__ == '__main__':
    input1_dir = "./data/6001.pickle"
    print("input1_dir", input1_dir)
    df_write = pd.DataFrame({"name": ["Tom", "Mary", "Jerry", "Mark"],
                             "age": [18, 22, 19, 31],
                             "gender": ["M", "F", "M", "M"]})
    df_write.to_pickle(input1_dir)
