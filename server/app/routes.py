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
        print('kill kill kill')
        try:
            self.video.release()
        except:
            print('probably there\'s no cap yet :(')
        cv2.destroyAllWindows()

    def release(self):
        print('kill kill kill')
        try:
            self.video.release()
        except:
            print('probably there\'s no cap yet :(')
        cv2.destroyAllWindows()

    def get_frame(self, is_crop='False'):
        success, frame = self.video.read()
        if success:
            frame = cv2.flip(frame, -1)
            with open('app/static/settings.json') as json_file:
                dd = json.load(json_file)
            if is_crop == 'True':
                d = dd['crop']
                frame = frame[int(d['y']):int(d['y']) + int(d['h']), int(d['x']):int(d['x'] + d['w'])]
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def take_picture(self, name, is_crop=False):
        success, frame = self.video.read()
        if success:
            frame = cv2.flip(frame, -1)
        if is_crop:
            with open('app/static/settings.json') as json_file:
                dd = json.load(json_file)
            d = dd['crop']
            frame = frame[int(d['y']):int(d['y']) + int(d['h']), int(d['x']):int(d['x'] + d['w'])]
        cv2.imwrite(name + '.jpg', frame)
        return Response(status=200)


cam = None


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    return 'hello pmf'


def gen(camera, is_crop='False'):
    while True:
        frame = camera.get_frame(is_crop)
        # Use generator function to output video stream, the content type of each request output is image/jpeg
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    global cam
    d = request.args.get('crop', default='False')
    print(d)
    cam = VideoCamera()
    return Response(gen(cam,d),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/takeimage', methods=['POST', 'GET'])
def takeimage():
    global cam
    cam.take_picture('screen')
    del cam
    return Response(status=200)


@app.route('/takeimage2', methods=['POST', 'GET'])
def takeimage2():
    global cam
    cam.take_picture('pos', True)
    del cam
    return Response(status=200)


@app.route('/savezones', methods=['GET', 'POST'])
def saveZones():
    d = request.get_json()
    data = d['zones']
    z1, z2 = [], []
    with open('app/static/settings.json') as json_file:
        dd = json.load(json_file)
    for a in dd['levels']:
        z1.append(a['z1'])
        z2.append(a['z2'])

    folder = d['folder']
    Path('store/' + folder).mkdir(parents=True, exist_ok=True)
    zones = {'zone': []}
    for i in range(len(data['x'])):
        z1_curr = z1[data['z'][i]]
        z2_curr = z2[data['z'][i]]
        zones['zone'].append({'ID': i, 'name': data['name'][i], 'x': int(data['x1'][i]),
                              'y': int(data['y1'][i]), 'x2': int(data['w'][i]), 'y2': int(data['h'][i]), 'Lvl': data['z'][i],
                              'z1': z1_curr, 'z2': z2_curr, 'type': data['type'][i]})
    with open('store/' + folder + '/zones.json', 'w') as outfile:
        json.dump(zones, outfile)
    return Response(status=200)


@app.route('/save_scenario', methods=['POST'])
def saveScenario():
    global cam
    d = request.get_json()
    data = d['scenario']
    folder = d['folder']
    Path('store/' + folder).mkdir(parents=True, exist_ok=True)
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
    print('sdsafdasfdasdsadadsad',folder)
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


@app.route('/crop', methods=['GET', 'POST'])
def crop():
    global cam
    d = request.get_json()
    img = cv2.imread("pos.jpg")
    cam = VideoCamera()
    return Response(gen(cam,d),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/save_pos_zone', methods=['GET', 'POST'])
def savePosZone():
    d = request.get_json()
    # print(d)
    # data = {'crop': []}
    # data['crop'].append({
    #     "y": d['y'],
    #     "x": d['x'],
    #     "w": d['w'],
    #     "h": d['h']
    # })
    with open('app/static/settings.json', 'r') as f:
        json_data = json.load(f)
        json_data['crop'] = {"y": int(d['y']), "x": int(d['x']), "w": int(d['w']), "h": int(d['h'])}
    with open('app/static/settings.json', 'w') as outfile:
        json.dump(json_data, outfile)
    return Response(status=200)


@app.route('/save_crop', methods=['GET', 'POST'])
def saveCrop():
    d = request.get_json()
    folder = d['folder']
    file = d['file']
    try:
        copy2('pos.jpg', 'store/' + folder)
    except IOError:
        os.chmod('app/', 777)  # ?? still can raise exception
        copy2('pos.jpg', 'store/' + folder)
    os.rename('store/' + folder + '/pos.jpg', 'store/' + folder + '/' + file + '.jpg')
    return Response(status=200)


@app.route('/save_zone_control', methods=['GET', 'POST'])
def saveZoneCtrl():
    d = request.get_json()
    data = d['zone']
    folder = d['folder']
    file = d['file']
    step = d['step']
    Path('store/' + folder).mkdir(parents=True, exist_ok=True)
    zones = {'zone': []}
    with open('store/' + folder + '/scenario.json', 'r') as infile:
        json_data = json.load(infile)
        for idx,j in enumerate(json_data['steps']):
            if j['name'] == step:
                print(json_data['steps'][idx])
                for idx2,o in enumerate(j['operations']):
                    if o['name'] == file:
                        json_data['steps'][idx]['operations'][idx2] = \
                            {'zone': 1, 'action': 'control', 'name': 'dasdsadss', 'ref_imgs':
                                'store/' + folder + '/' + file + '.jpg', 'control_zones': [
                                {'ID': '0', 'x1': data['x1'],
                                 'y1': data['y1'], 'x2': data['x1'] + data['x2'], 'y2':data['y1'] + data['y2']}
                      ] }
    with open('store/' + folder + '/scenario.json', 'w') as outfile:
        json.dump(json_data, outfile)
    return Response(status=200)
