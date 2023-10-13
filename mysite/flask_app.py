from flask import Flask
from flask import render_template, redirect, url_for, request
import requests
import time

app = Flask(__name__)

@app.route('/')
def Index():
    path = 'Index'
    return render_template('Index.html', path=path)
    
def slackMessage(text):
    url = 'https://hooks.slack.com/services/TMGE25VGT/B05GZRKLRU1/'
    url = url + '78IBMFJojDSDx6ON7wEXiOe7'
    payload = { "text" : text }

    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)