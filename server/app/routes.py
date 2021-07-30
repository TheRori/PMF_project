from flask import jsonify, Response, request
from pathlib import Path
import os
from app import app
import cv2
import json
from shutil import copy2


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
    global cam
    cam.take_picture()
    del cam
    return Response(status=200)


@app.route('/savezones', methods=['GET', 'POST'])
def saveZones():
    d = request.get_json()
    print(d)
    data = d['zones']
    folder = d['folder']
    print(folder)
    Path('store/' + folder).mkdir(parents=True, exist_ok=True)
    zones = {'zone': []}
    for i in range(len(data['x'])):
        zones['zone'].append({'ID': i, 'Name': data['name'][i], 'X': data['x'][i],
                              'Y': data['y'][i], 'W': data['w'][i], 'H': data['h'][i],
                              'Z': data['z'][i], 'Zone': data['type'][i]})
    with open('store/' + folder + '/zones.json', 'w') as outfile:
        json.dump(zones, outfile)
    return Response(status=200)


@app.route('/save_scenario', methods=['POST'])
def saveScenario():
    d = request.get_json()
    data = d['scenario']
    folder = d['folder']
    with open('store/' + folder + '/scenario.json', 'w') as outfile:
        json.dump(data, outfile)
    try:
        copy2('screen.jpg', 'store/' + folder)
    except IOError:
        os.chmod('app/', 777)  # ?? still can raise exception
        copy2('screen.jpg', 'store/' + folder)
    return Response(status=200)


@app.route('/reinit_img', methods=['GET'])
def reinit_img():
    try:
        copy2('screen.jpg', 'app/')
    except IOError:
        os.chmod('app/', 777)  # ?? still can raise exception
        copy2('screen.jpg', '/app')
    img = cv2.imread('screen.jpg')
    img[:] = (255, 255, 255)
    cv2.imwrite('screen.jpg', img)
    return Response(status=200)


@app.route('/load_img', methods=['GET'])
def load_img():
    folder = request.args.get('folder', '')
    print(folder)
    os.remove('screen.jpg')
    try:
        copy2('store/' + folder + '/screen.jpg', os.curdir)
    except IOError:
        copy2('store/' + folder + '/screen.jpg', os.curdir)
    return Response(status=200)


@app.route('/readzones', methods=['GET'])
def readZones():
    folder = request.args.get('folder', '')
    zones = {}
    with open('store/' + folder + '/zones.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route('/readscenario', methods=['GET'])
def readScenario():
    folder = request.args.get('folder', '')
    zones = {}
    with open('store/' + folder + '/scenario.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)


@app.route('/get_project_names', methods=['GET'])
def getProjectNames():
    names = os.listdir('store/')
    return jsonify(names)

