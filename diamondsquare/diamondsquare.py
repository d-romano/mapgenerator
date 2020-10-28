import random

class DiamondSquare:


	def __init__(self, size, roughness = .75, seed=None):
		self.size = size
		self.grid = self.generateGrid(size)

		# Help modify the scale for random int added to values
		self.roughness = roughness


	def fillGrid(self):
		''' Seed with random value then generate rest of values. ''' 

		# Remove later
		# 57 16 31 26

		# Seed initial corners with random values
		self.grid[0][0] = random.uniform(-1,1)
		self.grid[0][self.size-1] = random.uniform(-1,1)
		self.grid[self.size-1][0] = random.uniform(-1,1)
		self.grid[self.size-1][self.size-1] = random.uniform(-1,1)

		side = self.size -1

		while side >= 2:

			self.squareStep(self.size, side)
			self.diamondStep(self.size, side)

			# Shrink both random value and side len
			self.roughness = self.roughness / 2
			side = side // 2


	def getGrid(self):
		''' Return the value of the grid. '''
		return self.grid


	def mapGenerated(self):
		'''
			Checks if map has been generated. Generated map will not 
			have a 0 value.
		'''
		return self.grid[0][0]


	def squareStep(self, size, side):
		''' Find the center of each square and generate value.'''
		half = side // 2
		for r in range(0, size-1, side):
			for c in range(0, size-1, side):
				tl = self.grid[r][c]			# Top-left value.
				tr = self.grid[r][c+side]		# Top-right value.
				bl = self.grid[r+side][c]		# Bottom-left value.
				br = self.grid[r+side][c+side]	# Bottom-right value.

				avg = ((tl + tr + bl + br) / 4) #+ random seed value

				# Set the center of the current square to the average + random value
				self.grid[r+half][c+half] = avg + self.roughness


	def diamondStep(self, size, side):
		''' Find the center points of the squares and generate value.'''
		half = side // 2
		for r in range(0, size, half):
			for c in range((r + half)%side, size, side):
				t = self.grid[r-half][c] 		# Top value.
				l = self.grid[r][(c+half)%size]	# Left value.
				b = self.grid[(r+half)%size][c] # Bottom value.
				ri = self.grid[r][c-half]		# Right value.

				avg = ((t + l + b + ri) / 4) #Add seed value
				
				# Set current diamond point to grid
				self.grid[r][c] = avg + self.roughness


	def generateGrid(self, size):
		''' Generate a grid of size initialized with 0's.  '''
		grid = [[0 for _ in range(size)] for _ in range(size)]

		return grid