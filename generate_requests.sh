# Write code to generate requests
let NUM_REQUESTS=50

# Generate post requests to consume
for (( i = 0; i < NUM_REQUESTS; i++ )); do
	curl -H "Content-Type: application/json" -d "@requests/$i.json" -X POST http://localhost:5000/sessions/sendevents
done

# Get requests to get completed sessions
input="requests/players_completed.txt"
while IFS= read -r player_id
do
  curl -i http://localhost:5000/sessions/getcompleted/$player_id
done < "$input"
