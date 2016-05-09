#!flask/bin/python
from flask import Flask, jsonify, abort, request
import urllib2, json
from urllib2 import urlopen

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if not request.json:
        abort(400)

    docker_response = {
      'callback_url': request.json['callback_url'],
      'push_data': request.json['push_data'],
      'repository': request.json['repository']
    }

    try:
        callback_response = urlopen(docker_response['callback_url'])
        callback_data = json.loads(callback_response.read())
        payload = {
            'channel': '#website',
            'username': 'dockerhub',
            'text': 'New Docker Image Pushed',
            'icon_emoji': ':whale:',
            'attachments': [
                {
                    'title': 'State: ' + callback_data['state'],
                    'title_link': callback_data['target_url'],
                    'text': callback_data['description']
                }
            ]
        }
    except urllib2.HTTPError:
        payload = {
            'channel': '#website',
            'username': 'dockerhub',
            'text': 'Failed to push docker image',
            'icon_emoji': ':whale:'
        }

    json_payload = 'payload=' + json.dumps(payload)

    slack_request = urllib2.Request('https://hooks.slack.com/services/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')

    slack_response = urlopen(slack_request, json_payload)

    return json_payload

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
