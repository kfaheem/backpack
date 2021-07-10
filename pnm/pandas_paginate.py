import pandas as pd

dfs = pd.read_csv("some_df.csv", sep="\t", lineterminator="\r", skipinitialspace=True,
                  encoding="latin1", chunksize=1000, usecols=["col1", "col2"])

for df in dfs:
    print(df)
