# Desmos Bezier Renderer

A simple image/video to Desmos graph converter run locally

### Sample
![](github/sample.png)

### Result
![](github/result.png)

## Setup
#### This wont work out of the box on windows, the easiest way to do this on windows is to [download wsl](https://www.microsoft.com/store/productId/9N6SVWS3RX71) to run all the commands below. You can find it produces under the `\\wsl$\` file path on your pc.
Install dependencies
```sh
apt update
apt install git python3-dev python3-pip
```

Clone repository
```sh
git clone git@github.com:kevinjycui/DesmosBezierRenderer.git
cd DesmosBezierRenderer
```

Install requirements
```sh
python3 -m venv env
. env/bin/activate
pip3 install -r requirements.txt
```

Create a directory called `frames` and add images named `frame%d.png` where `%d` represents the frame-number starting from 1. To render just a single image, add a single image named `frame1.png` in the directory. Works best with 360p to 480p resolution (may have to lower the resolution further with more complex frames). 

You can change the `DYNAMIC_BLOCK`, `BLOCK_SIZE`, and `MAX_EXPR_PER_BLOCK` constants in `backend.py` to change the number of expressions the backend will send to the frontend per call (too much will cause a memory error, too little could kill the backend with too many requests). This only really matters if you are rendering a video. The `index.html` file also has some settings (`DOWNLOAD_IMAGES` and `MILLIS_PER_LINE`), if you would like to download each frame or slow down the render you should check that out.
```sh
mkdir frames
...
```

Run backend (This may take a while depending on the size and complexity of the frames). Should eventually show that the server is running on `localhost:5000`.
```sh
python3 backend.py
```

Load `index.html` into a web browser and put `f=1` into the first formula in the formula window. The image should start rendering or the video should start playing at a slow rate.
