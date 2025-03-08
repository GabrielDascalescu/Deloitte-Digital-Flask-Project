from flask import Flask, request, render_template, url_for
from index import MC
from os import listdir
import csv
import requests
import json

event_id = 3

app = Flask(__name__)

@app.route('/recommender-engine', endpoint = 'recommender')
def recommend():
    recommandations = []
    similar_ids = MC.find_similar_events(event_id, MC.X, k=5)
    event_title = MC.event_titles[event_id]

    for i in similar_ids:
        recommandations.append(MC.event_titles[i])

    return {"Since you liked" : event_title, "your recommandations are" : recommandations}

@app.route('/add-ratings', methods =['POST'])
def add_ratings():
    length = len(request.get_json())
    for index in range(len(request.get_json())):
        userid = request.get_json()[index]['User_id']
        eventid  = request.get_json()[index]['Event_id']
        rate = request.get_json()[index]['rating']
        data_to_append = [userid, eventid, rate]
        with open('Event-ratings.csv','a',newline = '') as file:
                writer = csv.writer(file)
                writer.writerow(data_to_append)
        file.close()
    return {"added rows# " :length}

@app.route('/add-events', methods = ['POST'])
def add_events():
    length = len(request.get_json())
    for index in range (len(request.get_json())):
        eventid = request.get_json()[index]['Event_ID']
        desc = request.get_json()[index]['Event_description']
        reward = request.get_json()[index]['Event_reward']
        data_to_append = [eventid, desc, reward]
        with open('Events.csv','a',newline = '') as file:
                writer = csv.writer(file)
                writer.writerow(data_to_append)
        file.close()

    return{"added rows#" : length}

if __name__ == '__main__':
    app.run(host ='0.0.0.0', port= 50100, debug = True)