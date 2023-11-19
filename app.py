from flask import Flask, send_from_directory, request, json
from flask_cors import CORS
from utils import database_search, database_apply, job_search, remove_job
import json
import os

print('app running')
app = Flask(__name__, static_folder='build', static_url_path='/')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/get-data/', methods=['GET', 'POST'])
def job_search_api():
    data = request.json
    print(data)
    if (data['latest'] == 'old'):
        latest_flag = False
    else:
        latest_flag = True
    if (data['type'] == 'Search'):
        res = database_search(data['title'], latest_flag)
    else:
        res = job_search(data['title'], latest_flag)
    # print(data)
    # print(res)
    return json.dumps(res)


@app.route('/api/apply-id/', methods=['GET', 'POST'])
def apply_job():
    data = request.json
    res = database_apply(data['job_id'])
    return json.dumps({'Data': 'Applied! Let us see'})


@app.route('/api/remove-id/', methods=['GET', 'POST'])
def remove_job_api():
    data = request.json
    print(data)
    res = remove_job(data['job_id'])
    return json.dumps({'Data': 'Applied! Let us see'})


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(port=5069)
