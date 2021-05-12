import os

dir = os.path.dirname(__file__)
number = 1
for filename in os.listdir("frames")[::-1]:
    path = os.path.join(dir, "frames", filename)
    if not filename.endswith(".png"):
        os.remove(path)
        print("Removed {}".format(filename))
    else:
        os.rename(path, os.path.join(dir, "frames", f"frame{str(number)}.png"))
        print("Renamed {} to frame{}.png".format(filename, number))
        number += 1
