from flask import jsonify, Response, request

from app import app
import cv2
import json


BOOKS = [
    {
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'r': True
    },
    {
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'r': False
    },
    {
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'r': True
    }
]

video = cv2.VideoCapture(0)


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    cv2.destroyAllWindows()
    m = BOOKS
    return jsonify(
        m
    )


def gen():
    """Video streaming generator function."""
    while True:
        rval, frame = video.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/takeimage', methods=['POST', 'GET'])
def takeimage():
    _, frame = video.read()
    cv2.imwrite('../../client/src/assets/salut.jpg', frame)
    return Response(status=200)


@app.route('/savezones', methods=['POST'])
def saveZones():
    data = request.get_json()
    zones = {}
    zones['zone'] = []
    for i in range(len(data['x'])):
        zones['zone'].append({'ID': i, 'X': data['x'][i], 'Y': data['y'][i], 'W': data['w'][i], 'H': data['h'][i]})
    with open('zones.txt', 'w') as outfile:
        json.dump(zones, outfile)
    return Response(status=200)


@app.route('/readzones', methods=['GET'])
def readZones():
    zones = {}
    with open('zones.txt') as json_file:
        data = json.load(json_file)
    return jsonify(data)


