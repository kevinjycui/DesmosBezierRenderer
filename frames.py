import os

# This should be the same information as in backend.py
FRAME_DIR = 'frames' # The folder where the frames are stored relative to this file
FILE_EXT = 'png' # Extension for frame files

dir = os.path.dirname(__file__)
number = 1
for filename in os.listdir(FRAME_DIR)[::-1]:
    path = os.path.join(dir, FRAME_DIR, filename)
    if not filename.endswith(FILE_EXT):
        os.remove(path)
        print("Removed {}".format(filename))
    else:
        os.rename(path, os.path.join(dir, FRAME_DIR, f"frame{str(number)}.{FILE_EXT}"))
        print("Renamed {} to frame{}.{}".format(filename, number, FILE_EXT))
        number += 1
