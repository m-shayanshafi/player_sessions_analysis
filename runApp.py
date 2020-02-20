from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, drop_table
from flask import Flask
from models.session import StartSession, EndSession, CompletedSession
from player_sessions_service import playerSession
from flask_apscheduler import APScheduler
from pytz import utc

COL_NAMES=["player_id", "session_id", "ts"]

class Config(object):

    JOBS = [
        {
            'id': 'deleteOldRecords',
            'func': 'runApp:deleteOldRecords',
            'args': (),
            'trigger': 'interval',
            'seconds': 30
        }
    ]
    SCHEDULER_API_ENABLED = True

KEYSPACE = "playersessions"

# Function that runs in background that deletes records periodically
def deleteOldRecords():

    import datetime
    from dateutil.relativedelta import relativedelta
    
    # Connect 
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect(KEYSPACE)
    
    # Get current time and date
    thisTime = datetime.datetime.now()
    oneYearAgo = thisTime.replace(year=(thisTime.year-1))
    oneYearAgo = str(oneYearAgo).strip('0')
    oneYearAgo = oneYearAgo.split('.',1)[0]

    # Delete records from each table
    delete_old_from_table('start_session', oneYearAgo, session)
    delete_old_from_table('end_session', oneYearAgo, session)
    delete_old_from_table('completed_session', oneYearAgo, session) 

# Delete table from old records
def delete_old_from_table(tableName, ts, session):

    rows = session.execute("SELECT player_id, session_id, ts FROM %s;" % (tableName))

    for row in rows:
        row_dict = dict(zip(COL_NAMES, row))
        session.execute("DELETE FROM %s WHERE player_id='%s' AND session_id='%s' AND ts < '%s';" % (tableName, row_dict["player_id"], row_dict["session_id"], ts))

# Set up keyspace to create app       
def create_app():

    app = Flask(__name__)
    app.debug = True
    app.register_blueprint(playerSession)
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
        """ % KEYSPACE)
    session = cluster.connect(keyspace=KEYSPACE)
    return app

app = create_app()

if __name__ == '__main__':
    
    connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)

    drop_table(StartSession)
    sync_table(StartSession, keyspaces=['playersessions'])

    drop_table(EndSession)
    sync_table(EndSession, keyspaces=['playersessions'])

    drop_table(CompletedSession)
    sync_table(CompletedSession, keyspaces=['playersessions'])

    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    app.run(debug=True, threaded=True)