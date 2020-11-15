'''
	Adapted from Ken Perlin's 
	improved perlin noise. Found at: https://mrl.cs.nyu.edu/~perlin/noise/
'''
import numpy as np
from numpy.ctypeslib import ndpointer
import math

import ctypes
import pathlib
import glob

def PerlinNoise(shape:(int,int), scale:float = 1, f:float = 10, l:float = 2.0, a:float = 10.0, p:float = .5, o:int = 4, randPerm: bool = False, seed = None):
	''' 
		Creates a heightmap of the requestion shape. Permutation table used in generation
		will either be Perlin's original table or a randomly generated one based on user request.
		Noise is generated using the current position, scale and octave (f) for each
		pixel in the height map. Scale determines how zoomed in or out the generated map appears.
	'''
	h,w = shape
	# Get name
	libname = libname = glob.glob(f"{pathlib.Path().absolute()}/build/*/dr_mapgen/perlin*.so")[0]
	c_lib = ctypes.CDLL(libname)

	c_lib.perlinNoise.argtypes = [ctypes.c_int, ctypes.c_double,
								 ctypes.c_double, ctypes.c_double,
								 ctypes.c_double, ctypes.c_double, 
								 ctypes.c_int, ndpointer(ctypes.c_int8), ndpointer(ctypes.c_double)]
	
	c_lib.perlinNoise.restype = None
	
	perm = getPermTable(randPerm, seed)
	grid = np.empty((h,w))

	c_lib.perlinNoise(ctypes.c_int(h), ctypes.c_double(scale), 
							ctypes.c_double(f), ctypes.c_double(l),
							ctypes.c_double(a), ctypes.c_double(p),
							ctypes.c_int(o), perm, grid)

	return grid
	

def getPermTable(randPerm, seed):
	# Generate random permutation or use Ken Perlin's perm table.
	'''
		Obtained from Ken Perlin's Documentation. Instead of copying the array again
		to fill with 512 values  I will use mod 256 when needed.
	'''	
	p = np.array([151,160,137,91,90,15,
	131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
	190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
    88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
	77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
	102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
	135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
	5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
	223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
	129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
	251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
	49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
	138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180], dtype=ctypes.c_int8)

	# Add seed if given or clear seed.
	np.random.seed(seed) if seed else np.random.seed()
	if randPerm: np.random.shuffle(p)

	return p
