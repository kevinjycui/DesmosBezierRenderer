import json
from flask import Flask
from flask_cors import CORS
from flask import request

from PIL import Image
import numpy as np
import potrace
import cv2

import multiprocessing
from time import time
import os
import sys
import getopt
import traceback


app = Flask(__name__)
CORS(app)


DYNAMIC_BLOCK = True # Automatically find the right block size
BLOCK_SIZE = 25 # Number of frames per block (ignored if DYNAMIC_BLOCK is true)
MAX_EXPR_PER_BLOCK = 7500 # Maximum lines per block, doesn't affect lines per frame (ignored if DYNAMIC_BLOCK is false)

FRAME_DIR = 'frames' # The folder where the frames are stored relative to this file
FILE_EXT = 'png' # Extension for frame files
COLOUR = '#2464b4' # Hex value of colour for graph output	

BILATERAL_FILTER = False # Reduce number of lines with bilateral filter
DOWNLOAD_IMAGES = False # Download each rendered frame automatically (works best in firefox)
USE_L2_GRADIENT = False # Creates less edges but is still accurate (leads to faster renders)
SHOW_GRID = True # Show the grid in the background while rendering

frame = multiprocessing.Value('i', 0)
height = multiprocessing.Value('i', 0, lock = False)
width = multiprocessing.Value('i', 0, lock = False)
frame_latex = 0


def help():
    print('backend.py -f <source> -e <extension> -c <colour> -b -d -l -g --static --block=<block size> --maxpblock=<max expressions per block>\n')
    print('\t-h\tGet help\n')
    print('-Render options\n')
    print('\t-f <source>\tThe directory from which the frames are stored (e.g. frames)')
    print('\t-e <extension>\tThe extension of the frame files (e.g. png)')
    print('\t-c <colour>\tThe colour of the lines to be drawn (e.g. #2464b4)')
    print('\t-b\t\tReduce number of lines with bilateral filter for simpler renders')
    print('\t-d\t\tDownload rendered frames automatically')
    print('\t-l\t\tReduce number of lines with L2 gradient for quicker renders')
    print('\t-g\t\tHide the grid in the background of the graph\n')
    print('-Optimisational options\n')
    print('\t--static\t\t\t\t\tUse a static number of expressions per request block')
    print('\t--block=<block size>\t\t\t\tThe number of frames per block in dynamic blocks')
    print('\t--maxpblock=<maximum expressions per block>\tThe maximum number of expressions per block in static blocks')


def get_contours(filename, nudge = .33):
    image = cv2.imread(filename)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if BILATERAL_FILTER:
        median = max(10, min(245, np.median(gray)))
        lower = int(max(0, (1 - nudge) * median))
        upper = int(min(255, (1 + nudge) * median))
        filtered = cv2.bilateralFilter(gray, 5, 50, 50)
        edged = cv2.Canny(filtered, lower, upper, L2gradient = USE_L2_GRADIENT)
    else:
        edged = cv2.Canny(gray, 30, 200)

    with frame.get_lock():
        frame.value += 1
        height.value = max(height.value, image.shape[0])
        width.value = max(width.value, image.shape[1])
    print('\r--> Frame %d/%d' % (frame.value, len(os.listdir(FRAME_DIR))), end='')

    return edged[::-1]


def get_trace(data):
    for i in range(len(data)):
        data[i][data[i] > 1] = 1
    bmp = potrace.Bitmap(data)
    path = bmp.trace(2, potrace.TURNPOLICY_MINORITY, 1.0, 1, .5)
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


def get_expressions(frame):
    exprid = 0
    exprs = []
    for expr in get_latex(FRAME_DIR + '/frame%d.%s' % (frame+1, FILE_EXT)):
        exprid += 1
        exprs.append({'id': 'expr-' + str(exprid), 'latex': expr, 'color': COLOUR, 'secret': True})
    return exprs


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
    return json.dumps({'result': block, 'number_of_frames': number_of_frames}) # Number_of_frames is the number of newly loaded frames, not the total frames


@app.route('/init')
def init():
    return json.dumps({'height': height.value, 'width': width.value, 'total_frames': len(os.listdir(FRAME_DIR)), 'download_images': DOWNLOAD_IMAGES, 'show_grid': SHOW_GRID})


if __name__ == '__main__':

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:e:c:bdlg", ['static', 'block=', 'maxpblock='])

    except getopt.GetoptError:
        print('Error: Invalid argument(s)\n')
        help()
        sys.exit(2)

    try:
        for opt, arg in opts:
            if opt == '-h':
                help()
                sys.exit()
            elif opt == '-f':
                FRAME_DIR = arg
            elif opt == '-e':
                FILE_EXT = arg
            elif opt == '-c':
                COLOUR = arg
            elif opt == '-b':
                BILATERAL_FILTER = True
            elif opt == '-d':
                DOWNLOAD_IMAGES = True
            elif opt == '-l':
                USE_L2_GRADIENT = True
            elif opt == '-g':
                SHOW_GRID = False
            elif opt == '--static':
                DYNAMIC_BLOCK = False
            elif opt == '--block':
                BLOCK_SIZE = int(arg)
            elif opt == '--maxpblock':
                MAX_EXPR_PER_BLOCK = int(arg)
        frame_latex =  range(len(os.listdir(FRAME_DIR)))

    except TypeError:
        print('Error: Invalid argument(s)\n')
        help()
        sys.exit(2)

    with multiprocessing.Pool(processes = multiprocessing.cpu_count()) as pool:
        print('Desmos Bezier Renderer')
        print('Junferno 2021')
        print('https://github.com/kevinjycui/DesmosBezierRenderer')

        print('-----------------------------')

        print('Processing %d frames... Please wait for processing to finish before running on frontend\n' % len(os.listdir(FRAME_DIR)))

        start = time()

        try:
            frame_latex = pool.map(get_expressions, frame_latex)
        except cv2.error as e:
            print('[ERROR] Unable to process one or more files. Remember image files should be named <DIRECTORY>/frame<INDEX>.<EXTENSION> where INDEX represents the frame number starting from 1 and DIRECTORY and EXTENSION are defined by command line arguments (e.g. frames/frame1.png). Please check if:\n\tThe files exist\n\tThe files are all valid image files\n\tThe name of the files given is correct as per command line arguments\n\tThe program has the necessary permissions to read the file.\n\nUse backend.py -h for further documentation\n')            

            print('-----------------------------')

            print('Full error traceback:\n')
            traceback.print_exc()
            sys.exit(2)

        print('\r--> Processing complete in %.1f seconds\n' % (time() - start))

        # with open('cache.json', 'w+') as f:
        #     json.dump(frame_latex, f)

        app.run()
