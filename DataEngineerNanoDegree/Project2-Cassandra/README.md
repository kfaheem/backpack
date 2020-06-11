<img src="cassandra.jpg" width="300" height="200" >

## <b>Project: Data Modeling with Cassandra</b>

### <b>Introduction:</b>
    
A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. There is no easy way to query the data to generate the results, since the data reside in a directory of CSV files on user activity on the app.

### <b>Project Overview:</b>

To achieve the ability to query the csv data, the data can be moved to a NOSQL database - Apache Cassandra. As opposed to a traditional RDBMS, a NOSQL database like Apache Cassandra offers the ability to store data without having to worry about a fixed schema. 
It also serves well for a usecase that entails storing data in huge volumes as it offers significant scalability. 

### <b>Datasets:</b>

For this project, you'll be working with one dataset: event_data. The directory of CSV files partitioned by date. Here are examples of filepaths to two files in the dataset:
event_data/2018-11-08-events.csv
event_data/2018-11-09-events.csv

### <b>Project Template:</b>

The project template includes one Jupyter Notebook file, in which:
•	you will process the event_datafile_new.csv dataset to create a denormalized dataset
•	you will model the data tables keeping in mind the queries you need to run
•	you have been provided queries that you will need to model your data tables for
•	you will load the data into tables you create in Apache Cassandra and run your queries

### <b>ETL Pipeline:</b>
1.	Implement the logic in section Part I of the notebook template to condense all data into a new CSV file.
2.	In Part II of the notebook, write CREATE and INSERT statements to load data from the file created in Part I into corresponding tables in Cassandra.
3.	Run SELECT statements to verify that the data is Inserted in the right tables successfully.
