# -*- coding: UTF-8 -*-

import pandas as pd
import json
from flask import render_template, request, jsonify, Flask
import flask
import traceback
import pymongo
from sklearn.cluster import KMeans
from collections import Counter
import time
import os
#import logging
#logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder = 'templates')

col = pymongo.MongoClient('mongodb+srv://oscar_tong:someiaadmin@dating-development.mdpwh.mongodb.net/someia-development?authSource=admin&replicaSet=atlas-bhevbk-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true')['development']['story']

def get_data():
    return(pd.DataFrame(col.find({"IS_PUBLIC" : True}, {"_id" : 0, "LATITUDE" : 1, "LONGITUDE" : 0})))
    
def stroy_clustering():
    data = get_data().to_numpy()
    out = {"Update time" : time.ctime()}
    iteration = 0
    for i in sorted([3+int((data.shape[0]/15 - 3)/i) if i != 0 else 3 for i in range(0, 5)]):
        iteration += 1
        kmeans = KMeans(n_clusters = i)
        kmeans.fit(data)
        out['Level %d'%iteration] = []
        count = Counter(kmeans.labels_)
        for j in range(i):
            out['Level %d'%iteration].append({
                "latitude" : kmeans.cluster_centers_[j][0],
                "longitude" : kmeans.cluster_centers_[j][1],
                "count" : count[j]
            })
    return(out)

@app.route('/make_stroy_clustering', methods=['GET'])
def clustering():
    result = stroy_clustering()
    with open('current_cluster.json', 'w') as f:
        json.dump(result, f)

@app.route('/', methods=['GET', 'POST'])
def main():
    return (render_template('welcome.html'))

@app.route('/get_stroy_clustering', methods=['GET'])
def get_clustering():
   if flask.request.method == 'GET':
       try:
            if "current_cluster.txt" in os.listdir():
                with open("current_cluster.json", 'r') as f:
                    return(json.load(f))
            else:
                clustering()
                with open("current_cluster.json", 'r') as f:
                    return(json.load(f))
       except:
           return jsonify({
               "trace": traceback.format_exc()
               })

if __name__ == "__main__":
   app.run()
