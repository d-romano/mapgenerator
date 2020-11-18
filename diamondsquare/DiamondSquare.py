import random
import numpy as np 
from numpy.ctypeslib import ndpointer
import ctypes
import pathlib
import glob
# Creates a wrapper that calls C++ code and returns a filled grid.
def DiamondSquare(scale:int, rough:float = 1.0, seed:int = None,  redNoise: bool = False):
	"""
	Generate a 2**n+1 x  2**n+1 image. Only has memory capacity to perform 
	(2**12+1)**2 images, albeit it slowly due to O(2^n) run time. Utilizes 32-bit 
	float values to minimize the amount of memory used (due to pythons datatype overhead).


	fillGrid(self) - Iniitializes the (2**n)**2 grid with all 0's and seeds the corner values
	with a python psuedo-random value between (-roughness, roughness) then runs DS algo to fill.

	squareStep(self, size, side, addVal) - Finds the center point of the current square being worked on
	and calcuates the center point based on the average of the four corner values + addVal.

	diamondStep(self, side, size, addVal) - Finds the four pixels in the cardinal directions of the square
	by getting the average of the ordinal directions of the square + addVal.

	medianFilter(filterSize) - Attempts to smooth the noise in a height map by replacing a pixel value in the center
	with the median of all its pixels in the area of filterSize x filterSize.

	"""
	# Opens shared c++ library.
	libname = glob.glob(f"{pathlib.Path().absolute()}/build/*/dr_mapgen/diamondsquare/*.so")[0]
	c_lib = ctypes.CDLL(libname)

	# Cast arg and return types to c-type values.
	c_lib.diamondSquare.argtypes = [ctypes.c_int, ctypes.c_double,
									ndpointer(ctypes.c_double), ctypes.c_int, ctypes.c_bool]
	c_lib.diamondSquare.restype = None

	# Create size from scale
	size = (2**scale) + 1
	grid = np.zeros((size,size))

	if not seed: seed = 0

	c_lib.diamondSquare(ctypes.c_int(size), ctypes.c_double(rough), grid, ctypes.c_int(seed), ctypes.c_bool(redNoise))

	return grid