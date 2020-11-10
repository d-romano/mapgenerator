import random
import numpy as np 



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
	size = 2**scale + 1

	# If seed entered then add to random, else clear seed 
	if seed:
		random.seed(seed)
	else:
		random.seed()

	# Remove later
	# 57 16 31 26
	grid = fillGrid(size, rough)

	if redNoise:
		grid = medianFilter(grid, size, 3)

	return grid


def fillGrid(size, rough):
	grid = np.zeros((size, size), dtype=np.float32)

	#  Holds base height for seeding
	baseHeight = .5
	# Seed initial corners with random values
	grid[0, 0] = random.uniform(-baseHeight, baseHeight)
	grid[0, size-1] = random.uniform(-baseHeight, baseHeight)
	grid[size-1, 0] = random.uniform(-baseHeight, baseHeight)
	grid[size-1, size-1] = random.uniform(-baseHeight, baseHeight)

	# Initialize the length of each side.
	side = size -1
	# Create range of additonal random value from roughness.
	addVal = rough
	while side >= 2:
		
		grid = squareStep(grid, size, side, addVal)
		grid = diamondStep(grid, size, side, addVal)
		# Shrink both random value and side len
		side = side // 2
		# Keeps a little residual noise
		addVal = max(addVal / 2, .01)

	return grid


def squareStep(grid, size, side, addVal):
	''' Find the center of each square and generate value.'''
	half = side // 2
	for r in range(0, size-1, side):
		for c in range(0, size-1, side):
			tl = grid[r,c]			# Top-left value.
			tr = grid[r,c+side]		# Top-right value.
			bl = grid[r+side,c]		# Bottom-left value.
			br = grid[r+side,c+side]	# Bottom-right value.

			avg = ((tl + tr + bl + br) / 4) 

			# Set the center of the current square to the average + random value
			grid[r+half,c+half] = avg + random.uniform(-addVal, addVal)

	return grid


def diamondStep(grid, size, side, addVal):
	''' Find the center points of the squares and generate value.'''
	half = side // 2
	for r in range(0, size, half):
		for c in range((r + half)%side, size, side):
			# Handle Wrap around cases for Y axis
			if r == 0:						# Handle Top value.
				t = grid[(size-1)-half,c]
			else:
				t = grid[r-half,c] 	

			if r == size-1:					# Handle Bottom value.
				b = grid[0+half, c] 	
			else:	
				b = grid[(r+half)%size,c] 	

			# Handle Wrap around cases for X axis.
			if c == 0:						# Handle Left value.	
				l = grid[r,(size-1)-half]
			else:
				l = grid[r,c-half]	
			if c == size-1:					# Handle Right value.
				ri = grid[r,0+half]	
			else:	
				ri = grid[r,(c+half)%size]	

			avg = ((t + l + b + ri) / 4)	
			# Set current diamond point to grid
			grid[r,c] = avg + random.uniform(-addVal, addVal)

	return grid


def medianFilter(grid, size, filterSize):
	''' Can be used to eliminate additional noise from image if needed.'''
	
	# Make copy of grid to avoid in-place errors.
	filterImg = np.array(grid, dtype=np.float32)
	# Array will hold values where the median lies.
	medArry = []
	# Center-point of nxn filter
	filtMid = filterSize // 2
	# Leave the edges as the same
	for y in range(1, size-1):
		for x in range(1, size-1):
			# Collect values within filter to generate median
			for m in range(filterSize):
				for n in range(filterSize):
					# If out of boundaries for the map wrap around to the other side memory errors.
					fX = ((x-filtMid) + n) % size
					fY = ((y-filtMid) + m) % size
					medArry.append(filterImg[fY][fX])
			# Sort and return median value and clear median Array.
			medArry.sort()
			#print(medArry)
			grid[y][x] = medArry[(filterSize*filterSize)//2]
			medArry.clear()
	return grid