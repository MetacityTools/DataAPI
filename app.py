from flask import Flask
from flask import render_template
from datetime import datetime

import os
import json


def read_config():
    with open('apiConfig.json') as f:
        return json.load(f)


def scan_filesystem(datasetDir):
    datasets = os.listdir(datasetDir)
    filtered = []
    for dataset in datasets:
        if os.path.join(datasetDir, dataset):
            filtered.append(dataset[:-5])
    return datasets


def get_dataset_list():
    config = read_config()
    dataset_names = scan_filesystem(config["datasetDir"])
    datasets = []
    for dataset_name in dataset_names:
        ts = os.path.getmtime(os.path.join(config["datasetDir"], dataset_name))
        datasets.append({
            "name": dataset_name,
            "url": os.path.join(config["rootAddress"], dataset_name),
            "timeChanged": datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        })
    return datasets


app = Flask(__name__)

@app.route("/")
def dataset_list():
    datasets = get_dataset_list()
    return render_template("index.html", datasets=datasets)

