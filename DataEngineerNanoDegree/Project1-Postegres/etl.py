import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def process_song_file(cur, filepath):
    """
    I read a given json file from its filepath into a dataframe & use its values to insert into songs & artists tables.
    :param cur: object - Postgres Cursor object
    :param filepath: str - Absolute file path of the song file
    :return:
    """
    try:
        # open song file
        df = pd.read_json(filepath, lines=True)

        # insert song record
        song_data = df[["song_id", "title", "artist_id", "year", "duration"]].values.tolist()[0]
        cur.execute(song_table_insert, song_data)

        # insert artist record
        artist_data = df[["artist_id", "artist_name", "artist_location",
                          "artist_latitude", "artist_longitude"]].values.tolist()[0]
        cur.execute(artist_table_insert, artist_data)

    except Exception as exception:
        logger.error("Received Exception in process_song_file function in covid_cases_by_country.py - {}".format(exception))
        raise exception


def process_log_file(cur, filepath):
    """
    I read a given json file from its filepath into a dataframe & use its values to insert into time & users tables.
    I then insert values into the song_play table using the values from the dataframe and also by performing
    an Inner join on the songs & artists table to get the song_id & artist_id.
    :param cur: object - Postgres Cursor object
    :param filepath: str - Absolute file path of the log file
    :return:
    """
    try:
        # open log file
        df = pd.read_json(filepath, lines=True)

        # filter by NextSong action
        df = df[df["page"] == "NextSong"]
        df.reset_index(inplace=True)

        # convert timestamp column to datetime
        t = pd.to_datetime(df["ts"], unit="ms")

        # insert time data records
        time_data = (t.dt.time.tolist(), t.dt.hour.tolist(), t.dt.day.tolist(), t.dt.week.tolist(), t.dt.month.tolist(),
                     t.dt.year.tolist(), t.dt.weekday.tolist())

        column_labels = ("start_time", "hour", "day", "week", "month", "year", "weekday")
        time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

        for i, row in time_df.iterrows():
            cur.execute(time_table_insert, list(row))

        # load user table
        user_df = df[["userId", "firstName", "lastName", "gender", "level"]].drop_duplicates(subset="userId")

        # insert user records
        for i, row in user_df.iterrows():
            cur.execute(user_table_insert, row)

        # insert songplay records
        for index, row in df.iterrows():

            # get songid and artistid from song and artist tables
            cur.execute(song_select, (row.song, row.artist, row.length))
            results = cur.fetchone()

            if results:
                songid, artistid = results
            else:
                songid, artistid = None, None

            # insert songplay record
            start_time = time_df["start_time"].values[index]
            songplay_data = (start_time, row.userId, row.level, songid, artistid, row.sessionId,
                             row.location, row.userAgent)
            cur.execute(songplay_table_insert, songplay_data)

    except Exception as exception:
        logger.error("Received Exception in process_log_file function in covid_cases_by_country.py - {}".format(exception))
        raise exception


def process_data(cur, conn, filepath, func):
    """
    I gather all the related files from the given filepath to be further used for ETL processing.
    :param cur: object - Postgres Cursor object
    :param conn: object - Postgres Connector object
    :param filepath: str - Root location where all json files are stored.
    :param func: function - ETL function for processing song/lof files.
    :return:
    """
    try:
        # get all files matching extension from directory
        all_files = []
        for root, dirs, files in os.walk(filepath):
            files = glob.glob(os.path.join(root, '*.json'))
            for f in files:
                all_files.append(os.path.abspath(f))

        # get total number of files found
        num_files = len(all_files)
        logger.info('{} files found in {}'.format(num_files, filepath))

        # iterate over files and process
        for i, datafile in enumerate(all_files, 1):
            func(cur, datafile)
            conn.commit()
            logger.info('{}/{} files processed.'.format(i, num_files))

    except Exception as exception:
        logger.error("Received Exception in process_data function in covid_cases_by_country.py - {}".format(exception))
        raise exception


def main():
    """
    I connect to the sparkifydb database, create the required tables in the database, extract data from the given
    filepaths and insert the data into the corresponding tables within sparkifydb.
    :return:
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
