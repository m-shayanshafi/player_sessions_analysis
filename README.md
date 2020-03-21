# Player Sessions Insights and Web Service

## Prerequisites

1. Python 3.8.1
2. Apache Cassandra
3. Cassandra Flask
4. FlaskAPScheduler

## Player Sessions Insights

This dataset loads the JSON dataset into player sessions using Apache Spark. The Jupyter Notebook (player_sessions_insights_1.ipynb.) answers the following questions:  

1. Sessions completed per country
2. Number of completed sessions.
3. Players by country.


## Sessions WebService API

Implements a REST API using Flask and Cassandra as the NOSQL database. The service consumes events that signify when a player session starts/ends. It provides an API endpoint that fetches the most recent completed sessions of a player. The following instructions are for test running an API:

### Step 1:Start Cassandra

1. Run the Cassandra database on your local machine.
```
cassandra -f
```

### Step 2:Run App

Run the webservice using the following:
```
python runApp.py
```

### Step 3: Generate JSON events
3. Generate a list of JSON set of events for batches of size 1-20.
```
bash generate_requests.py
``` 


### Step 4: Send Requests to WebService
4. Run script to send events and get metrics of completed events   
```
bash generate_requests.sh
```   