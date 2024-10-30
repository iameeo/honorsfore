from flask import Flask, render_template, redirect, request, jsonify
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
import requests, os, datetime
from http import HTTPStatus
from werkzeug.utils import secure_filename

app = Flask(__name__)
Mobility(app)

# Constants
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/TMGE25VGT/B05GZRKLRU1/'
SLACK_WEBHOOK_URL = SLACK_WEBHOOK_URL + 'NocJsMkkrzdBoFyssCDKJmfZ'

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Utility functions
def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def now_time():
    """Return the current timestamp in the format YYYYMMDDHHMMSS."""
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def get_creation_time(item):
    """Get the creation time of the file."""
    item_path = os.path.join(UPLOAD_FOLDER, item)
    return os.path.getctime(item_path)

def slack_message(text):
    """Send a message to Slack using a webhook."""
    if SLACK_WEBHOOK_URL:
        payload = {"text": text}
        response = requests.post(SLACK_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            raise ValueError(f"Slack request failed with error {response.status_code}: {response.text}")
    else:
        raise ValueError("Slack Webhook URL is not set")

# Routes
@app.route('/')
@mobile_template("{m/}index.html")
def index(template):
    path = 'index'
    slack_message(path)
    return render_template(template, path=path)

@app.route('/gallery/regist', methods=['GET'])
@mobile_template("{m/}gallery/regist.html")
def gallery_regist(template):
    path = 'gallery_regist'
    return render_template(template, path=path)

@app.route('/gallery/regist', methods=['POST'])
def gallery_regist_post():
    file = request.files.get('file')
    if file and allowed_file(file.filename):
        filename = secure_filename(now_time() + "_" + file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        slack_message(f"File uploaded: {filename}")
    else:
        return jsonify({"error": "Invalid file format"}), HTTPStatus.BAD_REQUEST
    
    return redirect('/')

@app.route('/gallery/get', methods=['GET'])
def gallery_get():
    files = sorted(os.listdir(UPLOAD_FOLDER), key=get_creation_time, reverse=True)
    return jsonify({"data": files, "status": HTTPStatus.OK})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)