# How to Use
## Install requiments
- Run this command in the terminal
```
pip install pillow numpy
```
## Run script
Run command in terminal
### Examples
- Default(640x480 30Frames)
```
py main.py
```
- Custom size(800x600 50Frames)
```
py main.py -w 800 -ht 600 -f 50
```
- File size(500KB)
```
py main.py -s 500
```
- File size & Custom output name
```
py main.py -s 300 -o my_noise.gif
```
### Options
- -w, --width
- -ht, --height
- -f, --frames
- -d, --duration
- -s, --max-size
- -o, --output
