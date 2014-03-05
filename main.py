from flask import Flask, request, Response, redirect, url_for
import sqlite3
import json
#from time import gmtime, strftime
from db_location import path

app = Flask(__name__)

@app.route("/")
def root():
	return redirect(url_for('static', filename = 'index.html'))

@app.route("/insertData")
def insertData():
	eventID = request.args.get("eventID")
	magnitude = request.args.get("magnitude")
	latitude = request.args.get("latitude")
	longitude = request.args.get("longitude")
	depth = request.args.get("depth")
	dateTime = request.args.get("dateTime")
	status = request.args.get("status")
	reliabilityCode = request.args.get("reliabilityCode")
	location = request.args.get("location")
	client = request.args.get("Client")
	
	#dateTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())

	data2insert = (eventID, magnitude, latitude, longitude, depth, dateTime, status, reliabilityCode, location, client)

	connection = sqlite3.connect(path)
	cur = connection.cursor()
	cur.execute('INSERT INTO seisms (eventID, magnitude, latitude, longitude, depth, dateTime, status, reliabilityCode, location, client) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data2insert)
	connection.commit()
	connection.close()

	data = {"eventID": eventID,
			"magnitude": magnitude,
			"latitude": latitude,
			"longitude": longitude,
			"depth": depth,
			"dateTime": dateTime,
			"status": status,
			"reliabilityCode": reliabilityCode,
			"location": location,
			"client": client}

	message = {"mesage": "Data inserted on the database"}
	message["event"] = data
	
	return Response(response=json.dumps(message),
	                    status=200,
	                    mimetype="application/json")


@app.route("/retrieveData")
def retrieveData():
	connection = sqlite3.connect(path)
	cur = connection.cursor()
	cur.execute("SELECT * FROM seisms")
	table = cur.fetchall()
	cur.close()

	data = []

	for e in table:

		event = {"eventID": e[0],
				"magnitude": e[1],
				"latitude": e[2],
				"longitude": e[3],
				"depth": e[4],
				"dateTime": e[5],
				"status": e[6],
				"reliabilityCode": e[7],
				"location": e[8],
				"client": e[9]}

		data.append(event)

	return Response(response=json.dumps(data),
	                    status=200,
	                    mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True)
    