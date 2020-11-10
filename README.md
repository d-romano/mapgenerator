# Map Generator
A GUI based applicaiton that will utilize the Diamond Square algorithm
to create a terrain map.

The aim of this project is to build an application that can be used 
to help build a world for table-top games.

Planned features are:
* Generate a map based on user inputted variables such as:
	* Map size
	* Terrain Roughness
	* Include water
	* Include Mountains

* Allow the map to be saved as an image.

Possible features:
* City/ Town generation.
* Landmark generation (Caves, monuments, etc).
* Allow uploading of a previously generated map for expansion.
* Additional generation algorithms (Perlin noise/ simplex noise)


## Components
There are three main components to this project.

### 1.) Map Terrain Generation
To generate the terrain there are 2 algorithms implemented that will generate height maps.

<<<<<<< HEAD
####Diamond Square
[Diamond-Square algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm)
![dsheatmap](https://user-images.githubusercontent.com/65517702/98038573-32598f80-1dd2-11eb-84ab-697468b11448.png)
####Perlin Noise
 adapted from [Ken Perlin's java reference](https://mrl.cs.nyu.edu/~perlin/noise/)
![pnheatmap](https://user-images.githubusercontent.com/65517702/98038575-32598f80-1dd2-11eb-825f-3c695c215a10.png)
=======
1. [Diamond-Square algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm)
	
    ![dsheatmap](https://github.com/d-romano/mapgenerator/raw/master/Images/dsheatmap.png)

2. Perlin Noise adapted from [Ken Perlin's java reference](https://mrl.cs.nyu.edu/~perlin/noise/)

    ![pnheatmap](https://github.com/d-romano/mapgenerator/raw/master/Images/pnheatmap.png)
>>>>>>> 9d694f6726cfdf1b610f1702176460c869ad674d

Both were implemented using NumPy for faster, more compact arrays as well as its C-like data types. 

### 2.) User Interface
For this portion I plan on using TKinter for a basic GUI that allows the user to enter the specifications
for their generated map. Once the image is generated it should display on the screen and give the user
an opportunity to save it or generate a new map.

### 3.) Image Generation
Calulates color for each pixel in the heightmap based on the current dictionary. Utilizes PIL and Numpy to create
a 3-D pixel raster that can be saved to specified file format. Previously was using .PPM format but has since been
depracated.


## Installation Process
* Clone from github using: `git clone https://github.com/d-romano/mapgenerator`
* Move to new clone directory
* Setup vitrual environment: 
	1.) Create using: `venv -m venv`
 	2.) Activate with: `source ./venv/bin/activate`
* Install requirements using: `pip install -r requirements.txt`

## How to use:
At the momement the modules must all be imported separately to be used. An example of a use case is:
```python

from diamondsquare import DiamondSquare as ds
from perlin import Perlin as pn
import WriteImage

# Creates heightmap of size 512x512, a 4x scale, frequency of 6 and uses the original Perlin Permutation table.
size = 512
pgrid = Perlin.PerlinNoise((size,size), scale=4, f=6, randPerm=False)

# Takes Width, Height and Heightmap and writes a jpg image
WriteImage.writeImg(size, size, pgrid, fType='jpg')
```

## Dev process
This application was buit on TKinter, NumPy, PIL and Python 3.7

## Use Cases:
To create a map to make table-top game session more immersive.

