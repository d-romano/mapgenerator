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

1. [Diamond-Square algorithm](https://en.wikipedia.org/wiki/Diamond-square_algorithm)
2. Perlin Noise adapted from [Ken Perlin's java reference](https://mrl.cs.nyu.edu/~perlin/noise/)

Both were implemented using NumPy for faster, more compact arrays as well as its C-like data types. 

### 2.) User Interface
For this portion I plan on using TKinter for a basic GUI that allows the user to enter the specifications
for their generated map. Once the image is generated it should display on the screen and give the user
an opportunity to save it or generate a new map.

### 3.) Image Generation
Convert a generated height map to a series of pixels based on a specificed colorscheme. For now the image is generated in a .ppm format with 24-bit colors. In the future I plan on updating this function with the ability to save to other file formats by utilizing PIL.

## Dev process
This application was buit on TKinter, NumPy, and Python 3.7

## Use Cases:
To create a map to make table-top game session more immersive.

