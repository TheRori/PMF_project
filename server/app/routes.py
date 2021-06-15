from flask import jsonify, Response, request

from app import app
import cv2

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


@app.route('/', methods=['GET'])
@app.route('/index')
def index():
    cv2.destroyAllWindows()
    m = BOOKS
    return jsonify(
        m
    )


def gen(video):
    """Video streaming generator function."""
    while True:
        rval, frame = video.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    video = cv2.VideoCapture(0)
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(video),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/takeimage', methods = ['POST','GET'])
def takeimage():
    video = cv2.VideoCapture(0)
    name = "hello"
    print(name)
    _, frame = video.read()
    cv2.imwrite('/Users/nicolasbovet/OneDrive - Université de Fribourg/Project python/PMF_project/client/src/assets/salut.jpg', frame)
    return Response(status = 200)