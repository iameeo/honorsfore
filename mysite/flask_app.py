from flask import Flask
from flask import render_template, redirect, url_for, request
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
import requests
import time

app = Flask(__name__)
Mobility(app)

@app.route('/')
@mobile_template("{m/}index.html")
def Index(template):
    path = 'index'
    return render_template(template, path=path)
    
def slackMessage(text):
    url = 'https://hooks.slack.com/services/TMGE25VGT/B05GZRKLRU1/'
    url = url + '78IBMFJojDSDx6ON7wEXiOe7'
    payload = { "text" : text }

    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)