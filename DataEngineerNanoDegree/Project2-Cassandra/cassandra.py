# Import Python packages
import pandas as pd
import cassandra
import re
import os
import glob
import numpy as np
import json
import csv

# checking your current working directory
print(os.getcwd())

# Get your current folder and subfolder event data
filepath = os.getcwd() + '/event_data'

# Create a for loop to create a list of files and collect each filepath
for root, dirs, files in os.walk(filepath):
    # join the file path and roots with the subdirectories using glob
    file_path_list = glob.glob(os.path.join(root, '*'))
    # print(file_path_list)

# initiating an empty list of rows that will be generated from each file
full_data_rows_list = []

# for every filepath in the file path list
for f in file_path_list:

    # reading csv file
    with open(f, 'r', encoding='utf8', newline='') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        next(csvreader)

        # extracting each data row one by one and append it
        for line in csvreader:
            # print(line)
            full_data_rows_list.append(line)

        # uncomment the code below if you would like to get total number of rows
# print(len(full_data_rows_list))
# uncomment the code below if you would like to check to see what the list of event data rows will look like
# print(full_data_rows_list)

# creating a smaller event data csv file called event_datafile_full csv that will be used to insert data into the \
# Apache Cassandra tables
csv.register_dialect('myDialect', quoting=csv.QUOTE_ALL, skipinitialspace=True)

with open('event_datafile_new.csv', 'w', encoding='utf8', newline='') as f:
    writer = csv.writer(f, dialect='myDialect')
    writer.writerow(['artist', 'firstName', 'gender', 'itemInSession', 'lastName', 'length',
                     'level', 'location', 'sessionId', 'song', 'userId'])
    for row in full_data_rows_list:
        if row[0] == '':
            continue
        writer.writerow((row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[12], row[13], row[16]))

# check the number of rows in your csv file
with open('event_datafile_new.csv', 'r', encoding = 'utf8') as f:
    print(sum(1 for line in f))

# This should make a connection to a Cassandra instance your local machine
# (127.0.0.1)

from cassandra.cluster import Cluster
cluster = Cluster(["127.0.0.1"])

# To establish connection and begin executing queries, need a session
session = cluster.connect()

# TO-DO: Create a Keyspace
session.execute("""CREATE KEYSPACE IF NOT EXISTS Sparkify WITH REPLICATION =
{"class": "SimpleStrategy", "replication_factor": 1}
""")

# TO-DO: Set KEYSPACE to the keyspace specified above
session.set_keyspace("Sparkify")

## TO-DO: Query 1:  Give me the artist, song title and song's length in the music app history that was heard during \
## sessionId = 338, and itemInSession = 4
session.execute("""
CREATE TABLE IF NOT EXISTS table1 (artist varchar, song varchar, length float, sessionId int, iteminSession int,
PRIMARY KEY(sessionId, iteminSession))
""")

# We have provided part of the code to set up the CSV file. Please complete the Apache Cassandra code below#
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
## TO-DO: Assign the INSERT statements into the `query` variable
        query = "INSERT INTO table1 (artist, song, duration, sessionId, iteminSession) "
        query = query + "VALUES (%s, %s, %s, %s, %s)"
        ## TO-DO: Assign which column element should be assigned for each column in the INSERT statement.
        ## For e.g., to INSERT artist_name and user first_name, you would change the code below to `line[0], line[1]`
        session.execute(query, (line[0], line[9], line[5], line[8], line[3]))

## TO-DO: Add in the SELECT statement to verify the data was entered into the table
session.execute("""SELECT artist, song, duration FROM table1 
WHERE sessionId = 338 AND itemInSession  = 4""")

## TO-DO: Query 2: Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name)\
## for userid = 10, sessionid = 182

session.execute("""
CREATE TABLE IF NOT EXISTS table2 (artist varchar, song varchar, firstName varchar,
lastName varchar, userId int, sessionId int, iteminSession int,
PRIMARY KEY(userId, sessionId, iteminSession))
""")

# We have provided part of the code to set up the CSV file. Please complete the Apache Cassandra code below#
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
## TO-DO: Assign the INSERT statements into the `query` variable
        query = "INSERT INTO table2 (artist, song, firstName, lastName, userId, sessionId, iteminSession) "
        query = query + "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        ## TO-DO: Assign which column element should be assigned for each column in the INSERT statement.
        ## For e.g., to INSERT artist_name and user first_name, you would change the code below to `line[0], line[1]`
        session.execute(query, (line[0], line[9], line[1], line[4], line[10], line[8], line[3]))

session.execute("""SELECT * FROM table2 
WHERE userId = 10 AND sessionId  = 182""")

## TO-DO: Query 3: Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'
session.execute("""
CREATE TABLE IF NOT EXISTS table3 (song varchar, firstName varchar,
lastName varchar, PRIMARY KEY(song)
""")

# We have provided part of the code to set up the CSV file. Please complete the Apache Cassandra code below#
file = 'event_datafile_new.csv'

with open(file, encoding = 'utf8') as f:
    csvreader = csv.reader(f)
    next(csvreader) # skip header
    for line in csvreader:
## TO-DO: Assign the INSERT statements into the `query` variable
        query = "INSERT INTO table3 (song, firstName, lastName) "
        query = query + "VALUES (%s, %s, %s)"
        ## TO-DO: Assign which column element should be assigned for each column in the INSERT statement.
        ## For e.g., to INSERT artist_name and user first_name, you would change the code below to `line[0], line[1]`
        session.execute(query, (line[9], line[1], line[4]))

session.execute("""SELECT * FROM table3 
WHERE song = "All Hands Against His Own"
""")

execute.query("DROP TABLE IF EXISTS table1")
execute.query("DROP TABLE IF EXISTS table2")
execute.query("DROP TABLE IF EXISTS table3")

session.shutdown()
cluster.shutdown()