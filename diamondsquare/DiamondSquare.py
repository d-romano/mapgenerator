import random
import numpy as np 


"""
	TODO:

	 - Change how to roughness scale affects the peaks and valleys of the generation.
	 - Change randomization tool to better allow users to remake maps based on seed.
	 - Attempt optimization. Currently application does not allow for an image larger than 2**15
"""


class DiamondSquare:
	def __init__(self, scale = 2, roughness = 1.0, seed=None):
		self.size = (2**scale)+1
		self.grid = None
		# Used to seed random to replicate results
		self.seed = seed
		# Help modify the scale for random int added to values
		self.rough = roughness


	def initGrid(self):
		''' initialize grid with zero then add seed values ''' 
		# Remove later
		# 57 16 31 26
		random.seed(12345)
		self.grid = np.zeros((self.size, self.size), dtype=np.float32)
		# Seed initial corners with random values
		self.grid[0,0] = random.uniform(-self.rough,self.rough)
		self.grid[0,self.size-1] = random.uniform(-self.rough,self.rough)
		self.grid[self.size-1,0] = random.uniform(-self.rough,self.rough)
		self.grid[self.size-1,self.size-1] = random.uniform(-self.rough,self.rough)

	def fillGrid(self):
		side = self.size -1

		addVal = 0
		lvl = 1
		while side >= 2:
			addVal = addVal / lvl+1
			self.squareStep(self.size, side, addVal)
			self.diamondStep(self.size, side, addVal)

			# Shrink both random value and side len
			side = side // 2
			
			lvl+=1

	def getGrid(self):
		''' Return the value of the grid. '''
		return self.grid


	def mapGenerated(self):
		'''
			Checks if map has been generated. Generated map will not 
			have a 0 value.
		'''
		return self.grid[0,0]


	def squareStep(self, size, side, addVal):
		''' Find the center of each square and generate value.'''
		half = side // 2
		for r in range(0, size-1, side):
			for c in range(0, size-1, side):
				tl = self.grid[r,c]			# Top-left value.
				tr = self.grid[r,c+side]		# Top-right value.
				bl = self.grid[r+side,c]		# Bottom-left value.
				br = self.grid[r+side,c+side]	# Bottom-right value.

				avg = ((tl + tr + bl + br) / 4) 

				# Set the center of the current square to the average + random value
				self.grid[r+half,c+half] = avg + random.uniform(-addVal, addVal)


	def diamondStep(self, size, side, addVal):
		''' Find the center points of the squares and generate value.'''

		half = side // 2
		for r in range(0, size, half):
			for c in range((r + half)%side, size, side):
				# Handle Wrap around cases for Y axis
				if r == 0:						# Handle Top value.
					t = self.grid[(size-1)-half,c]
				else:
					t = self.grid[r-half,c] 	

				if r == size-1:					# Handle Bottom value.
					b = self.grid[0+half, c] 	
				else:	
					b = self.grid[(r+half)%size,c] 	

				# Handle Wrap around cases for X axis.
				if c == 0:						# Handle Left value.	
					l = self.grid[r,(size-1)-half]
				else:
					l = self.grid[r,c-half]	
				if c == size-1:					# Handle Right value.
					ri = self.grid[r,0+half]	
				else:	
					ri = self.grid[r,(c+half)%size]	

				avg = ((t + l + b + ri) / 4)
				
				# Set current diamond point to grid
				self.grid[r,c] = avg + random.uniform(-addVal, addVal)