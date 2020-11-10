'''
	Adapted from Ken Perlin's 
	improved perlin noise. Found at: https://mrl.cs.nyu.edu/~perlin/noise/
'''
import numpy as np
import math

def PerlinNoise(shape:(int,int), scale:int = 1, f:int = 4, randPerm: bool = False):
	''' 
		Creates a heightmap of the requestion shape. Permutation table used in generation
		will either be Perlin's original table or a randomly generated one based on user request.
		Noise is generated using the current position, scale and octave (f) for each
		pixel in the height map. Scale determines how zoomed in or out the generated map appears.
	'''
	w,h = shape
	p = getPermTable(randPerm)
	grid = np.zeros(shape)
	

	for y in range(h):
		for x in range(w):
			grid[y][x] = _noise((x/ w/scale), (y/ h/scale), f, l, a, p,)
	return grid


def getPermTable(randPerm):
	# Generate random permutation or use Ken Perlin's perm table.
	if randPerm:
		p = np.random.choice(256, 256, replace=False)
	else:
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
		138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180], dtype=np.uint8)

	return p


def fade(t):
	'''
		Allows for smoother transition between values.
	'''
	return t * t * t * (t * (t * 6 - 15) + 10) 


def lerp(t, a, b):
	''' 
		Perform linear interpolation between A and B.
	'''
	return a + t * (b - a)


def grad(perm, x, y):
	# Get one of the 4 possible gradient vectors
	gradDir = perm & 3

	if gradDir == 0:
		return x + y
	elif gradDir  == 1:
		return -x + y
	elif gradDir == 2:
		return x - y
	elif gradDir == 3:
		return -x - y
	else: 0


def _noise(x, y, f = 10, l, a, p, o):
	""" 
		Information on frequency, lancularity, persistence, amplitude and affects on perlin noise from:
			-http://libnoise.sourceforge.net/glossary/#:~:text=also%3A%20Lacunarity%2C%20Persistence-,Persistence,produces%20%22rougher%22%20Perlin%20noise.
			-https://stackoverflow.com/questions/22380113/perlin-noise-input-values
	"""
	# Sum value of noise for each octave
	val = 0
	# Lower = more detail (zoomed in), lower = less detail(zoomed out).
	freq = f
	# Scale factor for each pass
	lancularity = .1
	# Max Height of each wave, works best in higher vals
	amp = 30
	# Lower = Simple (.5 appears to be sweetspot for maps similar to Diamond-Square)
	persistence = .50
	# Increase detail at cost of speed.
	octave = 8

	for i in range(octave):
		val += noise(x*freq, y*freq, p) * amp
		# Frequency increases x2 for each octave.
		freq *= lancularity
		amp *= persistence
	
	return val / octave


def noise(x, y, p):
	'''
		Get the noise value of the x and y coordinate or our matrix.
	'''
	#Get corner coordinates of chunk from our array of 256 permutations
	cX = int(math.floor(x)) & 255
	cY = int(math.floor(y)) & 255

	# Get pixel coordinates inside of chunk
	pX = x - math.floor(x)
	pY = y - math.floor(y)

	'''
		Get the gradient for the 4 corners of the main shape.
		Get the distance of the 4 corners from the current pixel
		Get the dot product of each corner gradient and its distance vector
		perform  bilinear interpolation.
		Product of that interpolation is the noise value of the pixel.
	'''
	g1 = p[(p[cX] + cY) % 256]		# Top Left Corner
	g2 = p[(p[(cX+1)%256] + cY) % 256]		# Top-Right Corner
	g3 = p[(p[cX] + cY + 1) % 256]		# Bottom Left Corner
	g4 = p[(p[(cX+1)%256] + cY +1) % 256]	# Bottom Right Corner

	# Get distances
	d1 = grad(g1, pX, pY)
	d2 = grad(g2, pX - 1, pY)
	d3 = grad(g3, pX, pY - 1)
	d4 = grad(g4, pX - 1, pY - 1)

	u = fade(pX)
	v = fade(pY)
	
	return lerp(v, lerp(u, d1, d2), lerp(u, d3,d4))