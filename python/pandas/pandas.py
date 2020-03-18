import pandas as pd


# Creating dataframe from object==========================================

obj1 = [{}, {}, {}]
df1 = pd.DataFrame(obj1, dtype={"col1": "str", "col2": "int", "col3": "bool"})  # passing dtype improves performance

obj2 = {"a": [], "b": [], "c": []}
df2 = pd.DataFrame(obj2)

df3 = pd.read_csv("")

df4 = pd.read_json("")


#  Create object from dataframe ==========================================

obj3 = df1.to_dict(orient="records")

csv_path = ""
obj4 = df3.to_csv(csv_path, index=True, header=True)

obj5 = df4.to_json()

# Dataframe operations ==========================================

df5 = df1[["col1", "col2"]][df1["col3"].isna]

df6 = df1[["col1", "col2"]][df1["col3"].notna]

df7 = df1[["col1", "col2"]][df1["col3"] == "xyz"]

df8 = df7.drop_duplicates(subset=["col1", "col2"])

df78 = df7.drop_na(subset="col9")

df89 = df7["col6"].to_frame()

df9 = df8[5:10]  # selects rows 5 to 10 and creates a new df

df = df9.groupby("col1")["col5"].mean()

df10 = df9.groupby("col1").agg(Mean=("col2", "mean"), Count=("col3", "count")).query("Mean > 3 & Count <=10")

df11 = df9.groupby("col1").agg({"col1": ["max", "min", "median"]})

df11["col10"].between("time1", "time2")

df11.sort_values("col2", ascending=False)

df11.head(), df11.tail(), df11.take(10), df11.nlargest(5), df11.nsmallest(5), df11.nunique(5)

df11["col1"].values("index") or df11.values("index")  # returns numpy array

df11.dtype.value_counts()
df11["col2"].value_counts()  # value_counts() does not work on a df, it needs a pandas series


df12 = pd.concat([df1, df2, df3], axis=0)  # one below another

df13 = pd.concat([df1, df2, df3], axis=1)  # side-by-side

df14 = df13.T  # Transpose

df15 = df14.stack()

df15["new_col"] = df15.apply(lambda x: x["cola"] - x["colb"], axis=1)

# Dataframe loops ==========================================

for _, row in df11.iterrows():
    row.col_new = row.col1 + row.col2

for row in df11.itertuples():
    row.col_new = row.col1 + row.col2

for index in range(len(df11)):  # faster than above 2 loops
    df11["new_col"] = df11["col1"].iloc[index] + df11["col2"].iloc[index]

df11["new_col"] = (df11["col1"] + df11["col2"]).sum()  # fastest

# Pandas Series ==========================================

obj6 = [1, 2, 3, 4, 4, 5]

ser = pd.Series(obj6, dtype="str")

ser.isdigit(), ser.split(), ser.lower()  # basically all string operations

# Pandas Pivot Table ==========================================

pivot_df = pd.pivot_table(df11, index=["col1", "col2"], aggfunc=["mean", "max", "min"])

pivot_view = pivot_df.pivot(index="col1", columns="col3", values="col5")




