import os
from flask import Flask ,request
from dotenv import load_dotenv
import psycopg2
from flask_cors import CORS
from flask import jsonify
from psycopg2 import extras
from psycopg2.extras import RealDictCursor
import json

load_dotenv()

app=Flask(__name__)

url=os.getenv("DATABASE_URL")

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

connection=psycopg2.connect(url)

cursordb=connection.cursor(cursor_factory = RealDictCursor)
"""Queries"""

CREATE_TABLE_TEAM=("""CREATE TABLE IF NOT EXISTS team
(
	team_id 	SERIAL	PRIMARY KEY,
	team_name	VARCHAR(25)	NOT NULL,
	stadium		VARCHAR(25)	NOT NULL
);""")

CREATE_TABLE_MATCH=("""
CREATE TABLE match
(
	match_id			SERIAL		PRIMARY KEY,
	home_team			INTEGER		NOT NULL,
	away_team			INTEGER		NOT NULL,
	home_score		INTEGER		DEFAULT null,
	away_score		INTEGER		DEFAULT null,
	match_date		DATE,
	FOREIGN KEY (home_team) REFERENCES team
		ON DELETE RESTRICT,
	FOREIGN KEY (away_team) REFERENCES team
		ON DELETE RESTRICT
);
""")

SELECT_ALL_TEAMS="""SELECT * FROM team"""

#ADD_RECORD_TEAM
INSERT_INTO_TEAM="INSERT INTO team(team_id,team_name,stadium) VALUES(%s,%s,%s)"
#ADD_RECORD_MATCH
INSERT_INTO_MATCH="INSERT INTO team(match_id,home_team,away_team,home_score,away_score,match_date) VALUES(%d:%m:%Y)"
@app.get("/")
def get():
    return jsonify("Home page")

@app.get("/epl_stats")
def getEplStats():
    return jsonify("English Premier League Statistics")


@app.post("/api/addTeam")
def addTeam():
    data=request.get_json()
    id=data["team_id"]
    name=data["team_name"]
    stadium=data["stadium"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_TABLE_TEAM)
            cursor.execute(INSERT_INTO_TEAM,(id,name,stadium))
            #team=cursor.fetchone()[0]
    return  {"message: ":"Was added successfully"},201     

def removeTeam(teamId):
    cursordb.execute(SELECT_ALL_TEAMS)
    teams=cursordb.fetchall()
    print("Teams: ",teams," has type of ",type(teams))
    print("Team to be deleted: ",teams[int(teamId)].team_name)
    for team in teams:
        if team["team_id"]==teamId:
            print("Team to be deleted founded")
            teams.remove(team)
            return False
        return team
    
#Endpoint for deleting an error 
@app.delete("/api/removeTeam/<teamid>")
def removeSingleTeam(teamid):
    rows_deleted=0
    cursordb.execute(SELECT_ALL_TEAMS)
    response_object={"response status":"succeeded"}
    response_object["message: "]= "Team removed"
    response_object["rows deleted: "]=str(rows_deleted)
    response_object["deleted id: "]=str(teamid)
    #response_object["name of team"]=removed_team[int(teamid)].team_name
    teams=cursordb.fetchall()
    print("Teams: ",teams," has type of ",type(teams))
    print("Team to be deleted: ",teams[int(teamid)].team_name)
    for team in teams:
        if team["team_id"]==teamid:
            print("Team to be deleted founded")
            cursordb.execute("DELETE FROM team WHERE team_id = %s",(teamid,))
            rows_deleted=cursordb.rowcount
            connection.commit()
            cursordb.close()
    return jsonify(response_object),201
"""

    #removed_team=removeTeam(teamid)
    
"""
   
    


@app.get("/teams")
def getAllTeams():
    with connection:
    	with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_TEAMS)
            teams_records=cursor.fetchall()
            #teams=json.dumps(teams_records)
            return jsonify({"status":"succeeded","teams":teams_records}),201

