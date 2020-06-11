## <b>Project: Data Lake with Redshift</b>

### <b>Introduction</b>

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

### <b>Project Description</b>

As the usecase involves massive datasets, having a relational database that is categorically designed for processing large datasets efficiently through Massive Parallel Processing would best fit our needs. 
Also, since the data resides in AWS S3, we need a Database that offers seamless integration with AWS resources. Which is why deploying a Redshift cluster would be apt for the given usecase. 
Redhsift's COPY protocol can be leveraged to transfer data S3 data into Redshift's staging tables, as seen in the diagram below. Since, the COPY protocol is intelligent enough to identify part files, each part file will be processes parallely. Thereby, making the data transfer process very efficient.
A star schema can then be created to establish optimal data modeling and querying.

### <b>Project Datasets</b>

Song Data Path     -->     s3://udacity-dend/song_data
Log Data Path      -->     s3://udacity-dend/log_data
Log Data JSON Path -->     s3://udacity-dend/log_json_path.json

### <b>Song Dataset</b>

The first dataset is a subset of real data from the Million Song Dataset(https://labrosa.ee.columbia.edu/millionsong/). Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. 
For example:

song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json

And below is an example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

### <b>Log Dataset</b>

The second dataset consists of log files in JSON format. The log files in the dataset with are partitioned by year and month.
For example:

log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json

And below is an example of what a single log file, 2018-11-13-events.json, looks like.

{"artist":"Pavement", "auth":"Logged In", "firstName":"Sylvie", "gender", "F", "itemInSession":0, "lastName":"Cruz", "length":99.16036, "level":"free", "location":"Klamath Falls, OR", "method":"PUT", "page":"NextSong", "registration":"1.541078e+12", "sessionId":345, "song":"Mercy:The Laundromat", "status":200, "ts":1541990258796, "userAgent":"Mozilla/5.0(Macintosh; Intel Mac OS X 10_9_4...)", "userId":10}

### <b>Tables</b>

<b>Fact Table</b>

<b>songplays</b> - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

<b>Dimension Tables</b>

<b>users</b> - users in the app
user_id, first_name, last_name, gender, level

<b>songs</b> - songs in music database
song_id, title, artist_id, year, duration

<b>artists</b> - artists in music database
artist_id, name, location, latitude, longitude

<b>time</b> - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday

### <b>Project Template</b>

Project Template include four files:

<b>1. create_table.py</b> is where you'll create your fact and dimension tables for the star schema in Redshift.

<b>2. etl.py</b> is where you'll load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.

<b>3. sql_queries.py</b> is where you'll define you SQL statements, which will be imported into the two other files above.

<b>4. README.md</b> is where you'll provide discussion on your process and decisions for this ETL pipeline.

### <b>ETL Pipeline</b>

1. Write CREATE statements in sql_queries.py
2. Complete the logic in create_tables.py to connect to the database and create these tables
3. Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. This way, you can run create_tables.py whenever you want to reset your database and test your ETL pipeline.
4. Launch a redshift cluster and create an IAM role that has read access to S3.
5. Add redshift database and IAM role info to dwh.cfg.
6. Test by running create_tables.py and checking the table schemas in your redshift database.
7. Implement the logic in etl.py to load data from S3 to staging tables on Redshift.
8. Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.
9. Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare your results with the expected results.
10. Delete your redshift cluster when finished.


### <b>ETL Architecture</b>
<img src="redshift_project.png" width="800" height="600" >