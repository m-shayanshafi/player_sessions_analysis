# Quiz

Developer quiz answers in Muhammad_Shayan_Quiz.pdf

# Task 1

Task 1 in Jupyter notebook implemented in player_sessions_insights_1.ipynb.

The output is also available in task1_pdf_jupyter.pdf. 

# Task 2: Player Web Service

## Prerequisites

1. Python 3.8.1
2. Apache Cassandra
3. Cassandra Flask
4. FlaskAPScheduler

## Step 1:Start Cassandra
1. Run the Cassandra database on your local machine.
```
cassandra -f
```

## Step 2:Run App
2. Run the webservice using the following:
```
python runApp.py
```

## Step 3: Generate JSON events
3. Generate a list of JSON set of events for batches of size 1-20.
```
bash generate_requests.py
``` 

## Step 4: Run the scripts
4. Run script to send events and get metrics of completed events   
```
bash generate_requests.sh
```   