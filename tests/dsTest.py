import unittest
import numpy as np
from diamondsquare import DiamondSquare as ds

'''
	Tests:
		- Create 2 grids with same seed, ensure they are equal
		- Create a grid of size GridSize, ensure shape of ndarray
		  is (GridSize, GridSize)
		- Ensure a grid with median filter is different from same grid
		  without median filter.
'''


class DiamondSqauareCase(unittest.TestCase):

	def setUp(self):
		''' Create a new grid with the following information '''
		self.size = 8
		# Large sizes need higher roughness to make use of filters since at some point filters all generate the same value.
		self.rough = 4 
		self.seed = 12345
		self.redNoise = True
		self.grid = ds.DiamondSquare(self.size, self.rough, self.seed, self.redNoise) 

	def teardown(self):
		''' No teardown needed for this test'''
		pass

	def test_size(self):
		''' Testing if the shape of generated grid is correct.'''
		numPx = (2**self.size) + 1
		self.assertEqual(self.grid.shape, (numPx, numPx))

	def test_seed(self):
		''' Testing grid seeding.'''
		identGrid = ds.DiamondSquare(self.size, self.rough, self.seed, self.redNoise) 
		# Same shape produced
		self.assertEqual(self.grid.shape, identGrid.shape)
		# Grid has same values
		self.assertTrue(np.allclose(self.grid, identGrid))

		# Generate a new grid without seed, should be different from orinal.
		diffGrid = ds.DiamondSquare(self.size, self.rough, None, self.redNoise)
		self.assertFalse(np.array_equal(self.grid, diffGrid))

	def test_filter(self):
		''' Test if median filter is working correctly. '''
		noFilter= ds.DiamondSquare(self.size, self.rough, self.seed, False)
		self.assertFalse(np.array_equal(self.grid, noFilter))


if __name__ == '__main__':
	unittest.main(verbosity=2)