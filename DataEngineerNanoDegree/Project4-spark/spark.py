from pyspark.sql import SpakrSession
from pyspark.sql.types import StructType, IntegerType, StructField, DoubleType, DateType
from pyspark.sql.functions import udf

spark = SpakrSession.builder.config("jar1", "jar2").appName("").getOrCreate()

# for reading a file without the schema known, we can use inferSchema while creating the dataframe

df1 = spark.read.csv("file_path.csv", inferSchema=True, header=True, sep=";",
                     mode="DROPMALFORMED")

# for reading a file with pre-defined Schema

schema = StructType([
    StructField("col_1", IntegerType()),
    StructField("col_2", DoubleType()),
    StructField("col_3", DateType())
])

df2 = spark.read.csv("file_path.csv", schema=schema, header=True, sep=";",
                     mode="DROPMALFORMED")


# =========================== #

# spark can read data from several places - local, s3, hdfs

df3 = spark.read.csv("s3a://....") # s3a for EC2, s3/s3a for EMR (s3 protocol is faster)
df4 = spark.read.csv("hdfs:///.....")

# spark can read/write from/to several databases
# SQL through jdbc
# NoSQL databases too

df5 = spark.read.format("jdbc").option("driver", "org.postgresql.Driver").\
    option("url", "jdbc:postgresql://localhost").option("dbtable", "schema.table").\
    option("user", "user").option("password", "password").load()

# convert spark df to pandas df

pandas_df = df5.limit(10).toPandas()

# to transform/add a column to a spark df

some_func = udf(lambda x: x*x)

df5 = df5.withColumn("column_name", some_func(df5.some_column))

# to run spark application on EMR, search for the spark-submit path by doing "which spark"
# then run spark-submit with its absolute path and the script --> /usr/bin/spark-submit spark.py

# copy data from local to EMR
# scp <local_path> <emr_name>:~/some_dir/sub_dir/

# copy data from EMR local file system to hdfs
# hdfs dfs -mkdir hdfs_dir
# hdfs dfs -copyFromLocal <EMR_local_path> <hdfs_path>

# write spark df to file
df5.write.save("file_path.csv", header=True, format="csv")

# drop duplicates & na

df5.dropDuplicates(subset="").drop_na(subset="")

# cast datatype of spark df column

df5.column_name.cast("float")


