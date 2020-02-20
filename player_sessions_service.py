from flask import Flask
from flask import make_response, jsonify
from flask import abort
from flask import request
from flask import Blueprint
from cassandra.cqlengine import connection
import sys
from models.session import StartSession, EndSession, CompletedSession
from cassandra.cluster import Cluster
import datetime

COL_NAMES=["player_id", "session_id", "ts"]

KEYSPACE='playersessions'

playerSession = Blueprint("playersession", __name__)
connection.setup(['127.0.0.1'], "cqlengine", protocol_version=3)
cluster = Cluster(['127.0.0.1'])
session = cluster.connect(KEYSPACE)    

# Get completed sessions
@playerSession.route('/sessions/getcompleted/<player_id>', methods=['GET'])
# Function to get completed sessions
def get_completed_sessions(player_id):	
	
	print("LOG: Got request for player: %s" % player_id)
	rows = session.execute("SELECT player_id, session_id, ts FROM completed_session WHERE player_id='%s' LIMIT 20" % (player_id))
	output = [dict(zip(COL_NAMES, row)) for row in rows]
	return jsonify({'completed_sessions': output})


# Consume events and add to DB
@playerSession.route('/sessions/sendevents', methods=['POST'])
def create_events():
	
	print("LOG:Received Batch of Events")
	if not request.json or not is_valid_request(request.json):
		abort(400)	

	event_statuses = []
	for event in request.json:		
		event_to_append, err = check_event_add_timestamp(event)
		if err == None:  						
			write_event(event_to_append)
			event_statuses.append({'status': 'Added to DB', 'event':event})
		else:
			event_statuses.append({'status': err, 'event':event})

	return make_response(jsonify({'event_statuses': event_statuses}), 201)

# Error handling
@playerSession.errorhandler(404)
def not_found(error):	
    return make_response(jsonify({'error': 'Player id not found'}), 404)		

# Add timestamp to received events
def check_event_add_timestamp(event):	

	player_id = event["player_id"]
	session_id = event["session_id"]

	# Check if start event exists for end. Otherwise return error
	if event["event"] == "end":

		rows = session.execute("SELECT player_id, session_id FROM start_session WHERE player_id='%s' AND session_id='%s' " % (player_id, session_id))	
		if (len(rows.current_rows))	!= 1:
			err = "No start event for end event. Failed to Write!"	
			return event, err

	event["ts"] = datetime.datetime.now()
	return event, None


# Error handling
def write_event(event):	

	if event["event"] == "start":

		session = StartSession.create(player_id=event["player_id"], session_id=event["session_id"], ts=event["ts"])	
		session.save()

	elif event["event"] == "end":

		session = EndSession.create(player_id=event["player_id"], session_id=event["session_id"], ts=event["ts"])
		session.save()

		session = CompletedSession.create(player_id=event["player_id"], session_id=event["session_id"], ts=event["ts"])
		session.save()

	return

# Check request for validity
def is_valid_request(events):

	for event in events:
		if not(event['session_id'] and event['player_id'] and (event['event']=='start' or event['event']=='end')):			
			return False
	return True