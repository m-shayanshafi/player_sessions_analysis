from flask import Flask
from flask import make_response, jsonify
from flask import abort
from flask import request
import sys


app = Flask(__name__)


completed_sessions = [
    	{
			"event": "start",
			"player_id": "0a2d12a1a7e145de8bae44c0c6e06629",
			"session_id": "4a0c43c9-c43a-42ff-ba55-67563dfa35d4",
		}, 
		{
			"event": "end",
			"player_id": "0a2d12a1a7e145de8bae44c0c6e06629",
			"session_id": "4a0c43c9-c43a-42ff-ba55-67563dfa35d4",
		}
]



# Get completed sessions
@app.route('/sessions/getcompleted/<int:player_id>', methods=['GET'])
def get_completed_sessions(player_id):	
	print("LOG: Got request for player: %d" % player_id)
	return jsonify({'completed_sessions': completed_sessions})

# Send events for completed sessions
@app.route('/sessions/sendevents', methods=['POST'])
def create_events():
	
	print("LOG:Received Events")

	if not request.json or not is_valid_request(request.json):
		abort(400)	

	event_statuses = []

	for event in request.json:		
		event_to_append = create_event(event)
		if event_to_append != None:  						
			write_event(event)
			event_statuses.append({'status': 'Added to DB', 'event':event})
		else:
			event_statuses.append({'status': 'Error while adding to DB', 'event':event})

	return make_response(jsonify({'event_statuses': event_statuses}), 201)


# Error handling
@app.errorhandler(404)
def not_found(error):	
    return make_response(jsonify({'error': 'Player id not found'}), 404)		

def create_event(event):
	# TODO: If start, generate timestamp.
	# TODO: If end, check if start record exists.Add record else error
	return event

def write_event(event):	

	# TODO: Add to Cassandra DB
	completed_sessions.append(event)
	return


def is_valid_request(events):

	for event in events:
		if not(event['session_id'] and event['player_id'] and (event['event']=='start' or event['event']=='end')):			
			return False

	return True
	

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    # app.run(HOST=XXX, PORT=XXX , threaded=True)
