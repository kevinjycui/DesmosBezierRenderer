# Desmos Bezier Renderer

A simple image/video to Desmos graph converter run locally. Rotoscopes images using Canny and Potrace edge detection as Bezier curves on Desmos Graphing Calculator.

![](github/figures.png)

## Setup
#### This guide won't work out of the box on Windows. The easiest way to do this on Windows is to [download WSL](https://www.microsoft.com/store/productId/9N6SVWS3RX71) to run all the commands below. You can find it produces under the `\\wsl$\Ubuntu-20.04\home` path on your PC.
Install dependencies
```sh
apt update
apt install git python3-dev python3-pip build-essential libagg-dev libpotrace-dev pkg-config
```

Clone repository
```sh
git clone https://github.com/kevinjycui/DesmosBezierRenderer.git
cd DesmosBezierRenderer
```

Install requirements
```sh
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```
Create a directory called `frames` and add images named `frame%d.png` where `%d` represents the frame-number starting from 1. To render just a single image, add a single image named `frame1.png` in the directory. Works best with 360p to 480p resolution (may have to lower the resolution further with more complex frames). 
```sh
mkdir frames
...
```
#### Settings
Constants in the `backend.py` file can be changed to optimise or customise your render via command-line arguments. Note that a "block" refers to what is passed from the backend to the frontend per HTTP request.
| Variable | Type | Description | Notes |
| --- | --- | --- | --- |
| `DYNAMIC_BLOCK` | Boolean | Automatically find the right block size | If unsure, leave as true
| `BLOCK_SIZE` | Integer | Number of frames per block | Ignored if `DYNAMIC_BLOCK` is true |
| `MAX_EXPR_PER_BLOCK` | Integer | Maximum lines per block, doesn't affect lines per frame | Ignored if `DYNAMIC_BLOCK` is false |
| `FRAME_DIR` | String | The folder where the frames are stored relative to this file | `'frames'` |
| `FILE_EXT` | String | Extension for frame files | `'png'`, `'jpg'`, etc. |
| `COLOUR` | String | Hex value of colour for graph output | Desmos blue is `'#2464b4'` |
| `DOWNLOAD_IMAGES` | Boolean | Download each rendered frame automatically (works best in Firefox) | If true, each frame is screenshotted automatically. Works best in Firefox, as chromium browsers will constantly prompt for downloads
| `USE_L2_GRADIENT` | Boolean | Creates less edges but is still accurate (leads to faster renders) | |
| `SHOW_GRID` | Boolean | Show the grid in the background while rendering | |

You can change the `DYNAMIC_BLOCK`, `BLOCK_SIZE`, and `MAX_EXPR_PER_BLOCK` to change the number of expressions the backend will send to the frontend per call (too much will cause a memory error, too little could kill the backend with too many requests). These only really matter if you are rendering a video.

Use `python3 backend.py -h` to learn more about these variables and how to set them. Run without any command-line arguments to create a rendering with the same settings as seen in [this video](https://www.youtube.com/watch?v=BQvBq3K50u8). To revert the code to be exactly as it was when the video was released, run `git checkout 47b10ea98b04b98ce46e54a46adde27bcb52e53e` first.

Run backend (This may take a while depending on the size and complexity of the frames). Should eventually show that the server is running on `localhost:5000`.
```sh
python3 backend.py
```

The following is an example of the output
```sh
Desmos Bezier Renderer
Junferno 2021
https://github.com/kevinjycui/DesmosBezierRenderer
-----------------------------
Processing 513 frames... Please wait for processing to finish before running on frontend

--> Processing complete in 7.4 seconds

 * Serving Flask app "backend" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [17/Sep/2021 01:28:46] "GET /init HTTP/1.1" 200 -
127.0.0.1 - - [17/Sep/2021 01:28:50] "GET /?frame=0 HTTP/1.1" 200 -
```

Load `index.html` into a web browser and put `f=1` into the first formula in the formula window. The image should start rendering or the video should start playing at a slow rate.

![](github/final.png)

## Attribution

©Copyright Junferno 2021. This program is licensed under the GNU General Public License. Please provide proper credit to the author (Junferno) in any public media that uses this software.