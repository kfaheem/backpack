import pandas as pd  # using "import modin.pandas as pd" is touted to be faster
import swifter
import seaborn as sns
import matplotlib.pyplot as plot


def create_df_from_object(object_or_file):
    """

    :param object_or_file:
    :return:
    """
    # if object_or_file is an object like [{}, {}, ..., {}] or {"": [], "": [], ...., }
    df1 = pd.DataFrame(object_or_file)

    # if object_or_file is a csv file
    df2 = pd.read_csv("csv_path.csv", dtype={"col1": "int", "col2": "float"}, nrows=10)
    # nrows can be leveraged to read sample data, passing dtype arg helps with improving performance

    # if object_or_file is an excel file
    df3 = pd.read_excel("excel_path.xlsx")

    # if object_or_file is a json file
    df3 = pd.read_json("json_path.json")

    # if object_or_file is an html file
    df4 = pd.read_html("html_path.html")

    # create df from pandas series
    df5 = df4["col1"].to_frame()


def create_object_from_df(df):
    """

    :param df:
    :return:
    """
    # to csv, with zip & without zip
    to_csv = df.to_csv("csv_path.csv", headers=True)
    to_gz = df.to_csv("csv_path.gz", compression="gzip", headers=True)
    # compression helps with saving disk/memory space

    # to_excel
    to_excel = df.to_excel("excel_path.xlsx")

    # to_html
    to_html = df.to_html("html_path.html")

    # to_latex
    to_latex = df.to_latex("html_path.latex")

    # to_markdown
    to_latex = df.to_markdown()  # markdown tables can be used in places like Readme.md etc

    # to a list of dictionaries
    to_dict = df.to_dict(orient="records")  # orient="records" removes index from the object

    # select df rows and convert to object
    df_to_csv = df[1:10].to_csv()


def loop_df(df):
    """

    :param df:
    :return:
    """
    # to perform transformation on a df, for example creating a new column from existing columns, we can
    # loop over the dataframe in several ways
    sum_total = 0

    for index, row in df.iterrows():
        sum_total += row["col1"] + row["col2"]

    for row in df.itertuples():
        sum_total += row.col1 + row.col2

    for index, row in range(len(df)):
        sum_total += row["col1"].iloc[index] + row["col1"].iloc[index]

    # for simpler operations like adding two columns, using pandas inbuilt functions would be the fastest option
    df["new_column"] = (df["col1"] + df["col2"]).sum()


def nearest_merge(df_a, df_b):
    # say you need to merge two dataframes on a timestamp column. The timestamps may have a difference of a few
    # seconds. If we need to merge the two dataframes, we can specify a timedelta which would merge timestamps
    # with the specified timedelta. For example, df_a has timestamp of x sec and df_b has a timestamp of x+10ms,
    # and if the specified timedelta is 10ms, the dataframes will be merged accordingly.

    df_c = pd.merge_asof(left=df_a, right=df_b, on="timestamp_column", by="column_to_match", how="left",
                         tolerance=pd.Timedelta('10ms'), direction='backward')


def merge_df(df_a, df_b):
    df_c = pd.merge(left=df_a, right=df_b, on="column_name", how="right", indicator=True)
    # indicator=True creates a column which tells you how the join happened. For example, if the value
    # existed in either dfs or both.


def concat_df(df1, df2, df3):
    df4 = pd.concat([df1, df2, df3], axis=0)  # concatenates dataframes one below another
    df5 = pd.concat([df1, df2, df3], axis=1)  # # concatenates dataframes side-by-side


def create_date_range(from_date, to_date):
    result = pd.date_range(from_date, to_date, freq="D")


def apply_df(df):
    df["new_column"] = df.apply(lambda row: row["col1"] + row["col2"], axis=1)

    # for a faster apply operation
    df["new_column"] = df.swifter.apply(lambda row: row["col1"] + row["col2"], axis=1)
    # using engine="numba" can also improve speed


def transform_df(df):
    df = df.tranform(func=lambda x: x * 10)  # multiplies each element in the df by 10

    df1 = df.groupby("some_column")["another_column"].tranform("mean")  # creates another column with mean values only


def filter_df(df):
    df1 = df[["col1", "col2"]][(df["col3"] == 100) & (df["col2"].isin([1, 2, 3, 4])) & (df["col1"].isna())]


def groupby_df(df):
    df1 = df.groupby(["col1", "col2"])["col3"].sum()

    df2 = df.groupby(["col1", "col2"]).agg(Mean=("col3", "mean"), Median=("col4", "median")).query(
        "Mean > 10 & Median = 5")

    df3 = df.groupby(["col1", "col2"]).agg({"col3": ["mean", "median", "max", "min", "sum"]})
    # creating aggregation for a single column


def transpose_df(df):
    df1 = df.T


def stack_df(df):
    df1 = df.stack()


def set_display_options(df):
    options = {
        "display.max_columns": 100,
        "display.min_columns": 50,
        "display.max_rows": 100,
        "display.min_rows": 50,
    }
    for key, value in options.items():
        pd.set_option(key, value)


def check_if_df_null(df):
    null_items = df.isnull().sum()


def sort_df(df):
    df1 = df.sort_values("column", ascending=False)


def drop_null_or_duplicates(df):
    df1 = df.drop_duplicates(subset=["col1", "col2"])

    df2 = df.dropna(subset="col3")


def unique_df(df):
    result = df["col1"].unique()  # return a numpy array, can be converted to list(result),
    # does not work on a dataframe object


def empty_df(df):
    result = df.empty  # True if df is empty, False otherwise


def count_dtype(df):
    result = df.dtypes.value_counts()


def select_dtypes_df(df):
    result_df = df.select_dtpes(include=["int", "float"])


def values_df(df):
    result = df.values(
        "index")  # returns numpy array, works on df as well as pandas series like df["col"].values("index")


def list_columns(df):
    result = df.columns.tolist  # returns a list of columns


def change_column_dtype(df):
    df["col1"] = df["col1"].as_type("float")


def replace_regex(df):
    df["col1"].replace("^f?g*[A-Z0-9]{3,4}", "replace with this", regex=True, inplace=True)


def string_operations(df):
    df["col1"].str.lstrip()

    series_obj = pd.Series([1, 2, 3, 4, 5], dtype="str")

    series_obj.str.isdigit()


def quickies(df):
    df.head()

    df.tail()

    df.take(10)

    df.nunique()

    df.nsmallest(n=10, columns=[""])  # or df["col1"].nsmallest(n=10)

    df.nlargest(n=10, columns=[""])


def pivot_table_df(df):
    pivot_table = pd.pivot_table(df, index=["col1, col2"], aggfunc=["mean", "sum"])

    pivot = pivot_table.pivot(index="col1", column="col2", values="col3")


def between_df(df):
    df["timestamp"].between("date-1", "date-2")


def is_equals(df1, df2):
    df1["col1"].isequals(df2["col2"])


def seaborn_charts(df):
    bar_plot = sns.barplot(data=df, x="col_name", y="col_name", style="summer", hue="summer")
    # to set/reset x, y & title axes names
    plot.xtitle("x title")
    plot.ytitle("y title")
    plot.title("my title")

    scatter_plot = sns.scatterplot(data=df, x="", y="")

    line_plot = sns.lineplot(data=df, x="", y=["", ""])

    count_plot = sns.countplot(data=df, x="")

    heat_map = sns.heatmap(data=["some_list"], cmap=["yellow", "red"])


