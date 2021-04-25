import json
from flask import Flask
from flask_cors import CORS
from flask import request

from PIL import Image
import numpy as np
import potrace
import cv2

import os


app = Flask(__name__)
CORS(app)


DYNAMIC_BLOCK = True

BLOCK_SIZE = 25
MAX_EXPR_PER_BLOCK = 7500
FRAME_DIR = 'frames'


def get_contours(filename):
    image = cv2.imread(filename)
    cv2.waitKey(0)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 30, 200)
    cv2.waitKey(0)
    
    contours, hierarchy = cv2.findContours(edged, 
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    return edged[::-1]


def get_trace(data):
    for i in range(len(data)):
        data[i][data[i] > 1] = 1
    bmp = potrace.Bitmap(data)
    path = bmp.trace()
    return path


def get_latex(filename):

    latex = []

    path = get_trace(get_contours(filename))

    for curve in path.curves:
        segments = curve.segments
        start = curve.start_point
        for segment in segments:
            x0, y0 = start
            if segment.is_corner:
                x1, y1 = segment.c
                x2, y2 = segment.end_point
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x0, x1, y0, y1))
                latex.append('((1-t)%f+t%f,(1-t)%f+t%f)' % (x1, x2, y1, y2))
            else:
                x1, y1 = segment.c1
                x2, y2 = segment.c2
                x3, y3 = segment.end_point
                latex.append('((1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)),\
                (1-t)((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f))+t((1-t)((1-t)%f+t%f)+t((1-t)%f+t%f)))' % \
                (x0, x1, x1, x2, x1, x2, x2, x3, y0, y1, y1, y2, y1, y2, y2, y3))
            start = segment.end_point

    return latex

frame_latex = []

for i in range(len(os.listdir(FRAME_DIR))):
    frame_latex.append(get_latex(FRAME_DIR + '/frame%d.png' % (i+1)))

with open('cache.json', 'w+') as f:
    json.dump(frame_latex, f)

@app.route('/')
def index():
    frame = int(request.args.get('frame'))
    if frame >= len(os.listdir(FRAME_DIR)):
        return {'result': None}
    block = []
    if not DYNAMIC_BLOCK:
        number_of_frames = min(frame + BLOCK_SIZE, len(os.listdir(FRAME_DIR))) - frame
        for i in range(frame, frame + number_of_frames):
            block.append(frame_latex[i])
    else:
        number_of_frames = 0
        total = 0
        i = frame
        while total < MAX_EXPR_PER_BLOCK:
            if i >= len(frame_latex):
                break
            number_of_frames += 1
            total += len(frame_latex[i])
            block.append(frame_latex[i])
            i += 1
    return json.dumps({'result': block, 'number_of_frames': number_of_frames})

app.run()