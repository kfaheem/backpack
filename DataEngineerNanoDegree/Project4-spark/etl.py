import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID'] = config['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY'] = config['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """

    :param spark:
    :param input_data:
    :param output_data:
    :return:
    """
    # get filepath to song data file
    song_data = "{}/song_data/*".format(input_data)

    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select(["song_id", "title", "artist_id", "year", "duration"])

    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist").parquet("{}/songs.parquet".format(output_data))

    # extract columns to create artists table
    artists_table = df.selectExpr("""SELECT artist_id, artist_name AS name, artist_location AS location,
    artist_latitude AS latitude, artist_longitude AS longitude""")

    # write artists table to parquet files
    artists_table.write.parquet("{}/artists.parquet".format(output_data))


def process_log_data(spark, input_data, output_data):
    """

    :param spark:
    :param input_data:
    :param output_data:
    :return:
    """
    # get filepath to log data file
    log_data = "{}/log_data/*".format(input_data)

    # read log data file
    df = spark.read.json(log_data)

    # filter by actions for song plays
    df = df.where("page"=="NextSong")

    # log_table temp_view
    df.createOrReplaceTempView("log_table")

    # extract columns for users table
    users_table = df.selectExpr("""SELECT userId AS user_id, firstName AS first_name, 
    lastName AS last_name, gender, level""")

    # write users table to parquet files
    users_table.write.parquet("{}/users.parquet".format(output_data))

    # create timestamp column from original timestamp column
    # get_timestamp = udf(lambda x: x*1000)
    # df = df.withColumn("timeStamp", get_timestamp("ts"))

    # create datetime column from original timestamp column
    # get_datetime = udf(lambda x: x*1)
    # df = df.select([year(""), month(""), dayofmonth(""), hour(""), weekofyear(""), date_format("")])

    # extract columns to create time table
    time_table = spark.sql("""
    SELECT  DISTINCT TIMESTAMP 'epoch' + se.ts/1000 \
    * INTERVAL '1 second'        AS start_time,
    EXTRACT(hour FROM start_time)    AS hour,
    EXTRACT(day FROM start_time)     AS day,
    EXTRACT(week FROM start_time)    AS week,
    EXTRACT(month FROM start_time)   AS month,
    EXTRACT(year FROM start_time)    AS year,
    EXTRACT(week FROM start_time)    AS weekday
    FROM    log_table                AS se;
    """)

    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet("{}/time.parquet".format(output_data))

    # read in song data to use for songplays table
    song_df = spark.read.parquet("{}/songs.parquet".format(output_data))

    # song_table temp view
    song_df.createOrReplaceTempView("song_table")

    # extract columns from joined song and log datasets to create songplays table
    songplays_table = spark.sql("""
    SELECT  DISTINCT TIMESTAMP 'epoch' + se.ts/1000 \
    * INTERVAL '1 second'       AS start_time,
    lt.userId                   AS user_id,
    lt.level                    AS level,
    st.song_id                  AS song_id,
    st.artist_id                AS artist_id,
    lt.sessionId                AS session_id,
    lt.location                 AS location,
    lt.userAgent                AS user_agent
    FROM log_table  AS lt
    JOIN song_table AS st
        ON (lt.artist = st.artist_name);
""")

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet("{}/songplays.parquet".format(output_data))


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend/output/"

    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
