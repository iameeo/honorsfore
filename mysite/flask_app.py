from flask import Flask, render_template, redirect, url_for, request
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
import requests
import os

app = Flask(__name__)
Mobility(app)

@app.route('/')
@mobile_template("{m/}index.html")
def index(template):
    path = 'index'
    slack_message(path)
    return render_template(template, path=path)

def slack_message(text):
    slack_url = 'https://hooks.slack.com/services/TMGE25VGT/B05GZRKLRU1/'
    slack_url = slack_url + 'NocJsMkkrzdBoFyssCDKJmfZ'

    if slack_url:
        payload = { "text": text }
        response = requests.post(slack_url, json=payload)
        if response.status_code != 200:
            raise ValueError(f'Request to slack returned an error {response.status_code}, the response is:\n{response.text}')
    else:
        raise ValueError("Slack Webhook URL not set")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)