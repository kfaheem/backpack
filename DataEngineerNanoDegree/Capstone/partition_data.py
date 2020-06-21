import pandas as pd
import os
path = os.getcwd()
print(path)
# df1 = pd.read_csv("{}/covid_county_data/county_population.csv".format(path))

# print(df1)

# df2 = pd.read_csv("{}/covid_county_data/covid_deaths.csv".format(path))
# # print(df2)
# columns = df2.columns.tolist()
# # print(columns)
#
# dates = columns[4:]
# # print(dates)

# for date in dates:
#     op_date = date.replace("/", "-")
#     op_path = "{}/covid_county_data/covid_deaths/{}.csv".format(path, op_date)
#
#     select = ['countyFIPS', 'County Name', 'State', 'stateFIPS', date]
#
#     df3 = df2[select][1:].to_csv(op_path, index=False, header=True)

# df4 = pd.read_csv("{}/covid_county_data/confirmed_cases.csv".format(path))
# # print(df4)
#
# columns = df4.columns.tolist()
#
# dates = columns[4:]
# # print(columns)
#
# for date in dates:
#     op_date = date.replace("/", "-")
#     op_path = "{}/covid_county_data/confirmed_cases/{}.csv".format(path, op_date)
#
#     select = ['countyFIPS', 'County Name', 'State', 'stateFIPS', date]
#
#     df5 = df4[select][1:].to_csv(op_path, index=False, header=True)