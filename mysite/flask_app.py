from flask import Flask, render_template, redirect, request, jsonify
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
import requests, os, datetime
from http import HTTPStatus

app = Flask(__name__)
Mobility(app)

UPLOAD_FOLDER = os.getcwd() + '\\mysite\\static\\upload'  # 절대 파일 경로
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

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
    print(request.files)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = now_time() + "_" + file.filename
        filepathtosave = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepathtosave)
    return redirect('/')

@app.route('/gallery/get', methods=['GET'])
def gallery_get():
    abs_path = os.path.join(UPLOAD_FOLDER)
    files = os.listdir(abs_path)
    return jsonify({"data": files, "status": HTTPStatus.OK})

def now_time():
    now = datetime.datetime.now()
    year = str(now.year)
    month = "0"+str(now.month)
    day = str(now.day)
    hour = str(now.hour)
    minute = str(now.minute)
    second = str(now.second)

    # ============================ 현재시간====================================
    # 10초 미만일 경우
    second = int(second)
    if second < 10: # 10초 미만이라면
        second = "0" + str(second)

    second = str(second)

     # 10분 미만일 경우
    minute = int(minute)
    if minute < 10: # 10분 미만이라면
        minute = "0" + str(minute)

    minute = str(minute)

    # 10시 미만일 경우
    hour = int(hour)
    if hour < 10: # 10시 미만이라면
        hour = "0" + str(hour)

    hour = str(hour)

    current_time = year+month+day+hour+minute+second   # 20210810215021

    return current_time

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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