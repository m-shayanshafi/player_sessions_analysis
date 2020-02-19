# Write code to generate requests
import json
import bz2
import random
import sys
import copy

dataFilePath = "assignment_data.jsonl.bz2"
outputRequestPath = "requests/"
numRequests = 50
completed_session_players = []

def get_start_end_record(record):

    # TODO Generate realistic records
    thisEvent = record["event"]
    record.pop('ts')
    randNumber = random.randint(1, 100)

    if randNumber > 30:
        
        new_record = copy.deepcopy(record)
        thisPlayer = new_record["player_id"]
        completed_session_players.append(thisPlayer)

        if thisEvent == "start":
            new_record["event"] = "end"
            return [record, new_record]
        else:
            new_record["event"] = "start"
            return [new_record, record]
    else:
        
        if thisEvent == "start":
            return [record]

def main():

    data = []
    generatedRequests = 0
    fileName = str(outputRequestPath) + str(generatedRequests) + ".json"
    g = open(fileName,"w")
    print("Generating POST requests...")

    with bz2.open(dataFilePath, "rt") as f:
        
        thisFileRecords = 0
        data = []
        numRecords = random.randint(1,20)        

        for line in f:
            
            record = json.loads(line)
            records = get_start_end_record(record)      
            
            if records != None:
                
                for r in records:
                    data.append(r)      
                thisFileRecords += len(records)


            if thisFileRecords >= numRecords:

                json_data = json.dumps(data)
                g.write(json_data)
                g.close()
                generatedRequests += 1
                if generatedRequests >= numRequests:
                    break
                fileName = str(outputRequestPath) + str(generatedRequests) + ".json"
                g = open(fileName,"w")
                numRecords = random.randint(1,20)
                thisFileRecords = 0
                data = []

    print("Generating player ids with completed sessions...")

    fileName = str(outputRequestPath) + "players_completed.txt"
    g = open(fileName,"w")

    for player in completed_session_players:
        g.write(player+"\n")

    g.close()


if __name__ == '__main__':
    main()

