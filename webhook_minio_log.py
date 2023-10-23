# application to act as webhook for minio server and show the data received from minio server
import os
import datetime
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

GRAYLOG_IP = os.environ.get('GRAYLOG_IP')
GRAYLOG_PORT = os.environ.get('GRAYLOG_PORT')

if not GRAYLOG_IP or not GRAYLOG_PORT:
    print('Error: Graylog IP or port not found in environment variables.')
    exit(1)

@app.route('/', methods=['POST'])
def webhook():
    # get the timestamp from the request and convert it to timestamp
    # remove T and Z from the timestamp sample 2023-10-10T07:20:11.412345545Z
    logTime = request.json['time'].replace('T', ' ').replace('Z', '')[:-6]
    # get the utc timestamp from the logTime
    logTimestamp = datetime.datetime.strptime(logTime, '%Y-%m-%d %H:%M:%S.%f')
    # add the utc timezone to the timestamp
    logTimestamp = logTimestamp.replace(tzinfo=datetime.timezone.utc).timestamp()
    payload = {
        "Version": request.json['version'], # version is changed to Version as gray log GELP HTTP input requires capital V for version
        "host": request.remote_addr,
        "short_message": f"minio-audit-log",
        "full_message": request.json,
        "timestamp": logTimestamp
    }
    # add this json to payload
    payload.update(dict(request.json))
    # extract api dictionary from request json
    # send request to graylog server with the above body
    print(f"sending payload: {payload} with timestamp: {datetime.datetime.now().timestamp()}")
    graylog_req = requests.post(f'http://{GRAYLOG_IP}:{GRAYLOG_PORT}/gelf', json=payload)
    # show the response from graylog server
    print(f"gray log request status: {graylog_req}")
    return jsonify({'success': True}), 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
