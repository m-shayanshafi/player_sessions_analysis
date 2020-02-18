from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, drop_table
from flask import Flask
from models.session import Session
from player_sessions_service import playerSession

KEYSPACE = "playersessions"

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
    drop_table(Session)
    sync_table(Session, keyspaces=['playersessions'])
    app.run(debug=True, threaded=True)
    # app.run(host="0.0.0.0", port=8081)