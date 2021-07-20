from flask import jsonify, Response, request

import os
from app import app
import cv2
import json


class VideoCamera(object):
    def __init__(self):
        # Get real-time video stream through opencv
        # url source see my last blog
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        try:
            self.video.release()
        except:
            print('probably there\'s no cap yet :(')
        cv2.destroyAllWindows()

    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def take_picture(self):
        _, frame = self.video.read()
        cv2.imwrite('screen.jpg', frame)

        return Response(status=200)


cam = None


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return 'hello pmf'


def gen(camera):
    while True:
        frame = camera.get_frame()
        # Use generator function to output video stream, the content type of each request output is image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    global cam
    cam = VideoCamera()
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/takeimage', methods=['POST', 'GET'])
def takeimage():
    cam.take_picture()
    return Response(status=200)


@app.route('/savezones', methods=['POST'])
def saveZones():
    data = request.get_json()
    print('hello')
    zones = {'zone': []}
    for i in range(len(data['x'])):
        zones['zone'].append({'ID': i, 'X': data['x'][i], 'Y': data['y'][i], 'W': data['w'][i], 'H': data['h'][i],
                              'Zone': data['type'][i]})
    with open('zones.json', 'w') as outfile:
        json.dump(zones, outfile)
    img = cv2.imread('screen.jpg')
    img[:] = (255, 255, 255)
    cv2.imwrite('screen.jpg', img)
    global cam
    del cam
    return Response(status=200)


@app.route('/readzones', methods=['GET'])
def readZones():
    zones = {}
    with open('zones.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)
