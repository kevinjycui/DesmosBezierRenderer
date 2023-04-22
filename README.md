# Desmos Bezier Renderer

A simple image/video to Desmos graph converter run locally. Rotoscopes images using Canny and Potrace edge detection as Bezier curves on Desmos Graphing Calculator.

![](github/figures.png)

## Setup
#### This guide won't work out of the box on Windows. The easiest way to do this on Windows is to [install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) to run all the commands below. You can find it produces under the `\\wsl$\Ubuntu-20.04\home` path on your PC.
Install dependencies
```sh
sudo apt update
sudo apt install git python3-dev python3-pip build-essential libagg-dev libpotrace-dev pkg-config
```

Clone repository
```sh
git clone https://github.com/kevinjycui/DesmosBezierRenderer.git
cd DesmosBezierRenderer
```

Install requirements
```sh
python -m venv env
. env/bin/activate
pip install wheel
pip install -r requirements.txt
```
Replace the images in the `frames` directory with your own and name each image `frame%d.png` where `%d` represents the frame-number starting from 1. To render just a single image, add a single image named `frame1.png` in the directory. Works best with 360p to 480p resolution (may have to lower the resolution further with more complex frames).
```sh
mkdir frames
...
```
#### Settings
Constants in the `backend.py` file can be changed to optimise or customise your render via command-line arguments.

```sh
$ python backend.py -h
backend.py -f <source> -e <extension> -c <colour> -b -d -l -g --static --block=<block size> --maxpblock=<max expressions per block>

	-h	Get help

-Render options

	-f <source>	The directory from which the frames are stored (e.g. frames)
	-e <extension>	The extension of the frame files (e.g. png)
	-c <colour>	The colour of the lines to be drawn (e.g. #2464b4)
	-b		Reduce number of lines with bilateral filter for simpler renders
	-d		Download rendered frames automatically (only available if rendering quick.html)
	-l		Reduce number of lines with L2 gradient for quicker renders
	-g		Hide the grid in the background of the graph (only available if rendering quick.html)

-Optimisational options

	--static					Use a static number of expressions per request block
	--block=<block size>				The number of frames per block in dynamic blocks
	--maxpblock=<maximum expressions per block>	The maximum number of expressions per block in static blocks

-Miscellaneous

	--yes	Agree to EULA without input prompt
```

You can use the optimisational options to change the number of expressions the backend will send to the frontend per call (too much will cause a memory error, too little could kill the backend with too many requests). Note that a "block" refers to what is passed from the backend to the frontend per HTTP request. These only really matter if you are rendering a video.

Use `python backend.py -h` to see the above help message. Run without any command-line arguments to create a rendering with the same settings as seen in [this video](https://www.youtube.com/watch?v=BQvBq3K50u8). 

#### Running the command

Run backend (This may take a while depending on the size and complexity of the frames). It should eventually show that the server is running on `localhost:5000`.
```sh
python backend.py
```

The following is an example of the output
```sh
$ python backend.py 
  _____                                
 |  __ \                               
 | |  | | ___  ___ _ __ ___   ___  ___ 
 | |  | |/ _ \/ __| '_ ` _ \ / _ \/ __|
 | |__| |  __/\__ \ | | | | | (_) \__ \
 |_____/ \___||___/_| |_| |_|\___/|___/

                   BEZIER RENDERER
Junferno 2021
https://github.com/kevinjycui/DesmosBezierRenderer

 = COPYRIGHT =
©Copyright Junferno 2021-2023. This program is licensed under the [GNU General Public License](https://github.com/kevinjycui/DesmosBezierRenderer/blob/master/LICENSE). Please provide proper credit to the author (Junferno) in any public media that uses this software. Desmos Bezier Renderer is in no way, shape, or form endorsed by or associated with Desmos, Inc.

 = EULA =
By using Desmos Bezier Renderer, you agree to comply to the [Desmos Terms of Service](https://www.desmos.com/terms). The Software and related documentation are provided “AS IS” and without any warranty of any kind. Desmos Bezier Renderer is not responsible for any User application or modification that constitutes a breach in terms. User acknowledges and agrees that the use of the Software is at the User's sole risk. The developer kindly asks Users to not use Desmos Bezier Renderer to enter into Desmos Math Art competitions, for the purpose of maintaining fairness and integrity.

                                      Agree (y/n)? y
-----------------------------
Processing 513 frames... Please wait for processing to finish before running on frontend

--> Processing complete in 4.4 seconds

 * Serving Flask app "backend" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

Load `index.html` into a web browser and put `f=1` into the first formula in the formula window. The image should start rendering or the video should start playing at a slow rate. 

Alternatively, you can load `quick.html` for a **quicker rendering** with **more consistent rendering time per frame** that also allows for the use of the automatic download (`-d`) and gridline removal (`-g`) options. This however will also lower the quality, cause frames to disappear immediately after rendering, and will not show equations in the left sidebar. The renders seen in the video [this video](https://www.youtube.com/watch?v=BQvBq3K50u8) use `index.html` whereas [this video](https://www.youtube.com/watch?v=c38ob_YC0IA) uses `quick.html`.

![](github/final.png)

## Copyright

©Copyright Junferno 2021-2023. This program is licensed under the [GNU General Public License](https://github.com/kevinjycui/DesmosBezierRenderer/blob/master/LICENSE). Please provide proper credit to the author (Junferno) in any public media that uses this software. Desmos Bezier Renderer is in no way, shape, or form endorsed by or associated with Desmos, Inc.

## EULA
```
By using Desmos Bezier Renderer, you agree to comply to the [Desmos Terms of Service](https://www.desmos.com/terms). The Software and related documentation are provided “AS IS” and without any warranty of any kind. Desmos Bezier Renderer is not responsible for any User application or modification that constitutes a breach in terms. User acknowledges and agrees that the use of the Software is at the User's sole risk. The developer kindly asks Users to not use Desmos Bezier Renderer to enter into Desmos Math Art competitions, for the purpose of maintaining fairness and integrity.
```