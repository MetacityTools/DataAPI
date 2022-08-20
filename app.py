from flask import Flask
from flask import render_template
from datetime import datetime

import os
import json


CONFIG = "apiConfig.json"
DEBUG = True
if DEBUG:
    CONFIG = "devConfig.json"


def read_config():
    # get directory of this file
    dirname = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dirname, CONFIG)) as f:
        return json.load(f)


def scan_filesystem(datasetDir):
    datasets = os.listdir(datasetDir)
    filtered = []
    for dataset in datasets:
        if os.path.exists(os.path.join(datasetDir, dataset, 'layout.json')):
            filtered.append(dataset)
    return filtered


def get_description(datasetDir):
    if os.path.exists(os.path.join(datasetDir, 'description.json')):
        with open(os.path.join(datasetDir, 'description.json')) as f:
            return json.load(f)  


def get_dataset_list():
    config = read_config()
    dataset_names = scan_filesystem(config["datasetDir"])
    datasets = []
    for dataset_name in dataset_names:
        ts = os.path.getmtime(os.path.join(config["datasetDir"], dataset_name, 'layout.json'))
        datasets.append({
            "name": dataset_name,
            "url": os.path.join(config["rootAddress"], dataset_name),
            "timeChanged": datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),
            "description": get_description(os.path.join(config["datasetDir"], dataset_name))    
        })
    return datasets


app = Flask(__name__)

@app.route("/")
def dataset_list():
    datasets = get_dataset_list()
    return render_template("index.html", datasets=datasets)

