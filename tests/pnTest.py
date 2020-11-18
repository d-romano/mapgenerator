import numpy as np
import unittest
from perlin import Perlin as pn


'''
	Tests:
		- Create second perlin noise grid with orig permutation.
		  Ensure shape is the same and that the created heightmap is equal.
		- Create perlin image with random permutation, ensure its different from original
		- Create 2 new perlin images with the same seed, ensure heightmap is equal
'''

class PerlinNoiseCase(unittest.TestCase):
	def setUp(self):
		self.shape = 8
		self.scale = 3
		self.f = 4
		self. l = 2
		self.a = 15
		self.p = .2
		self.o = 8
		self.rand = False
		self.seed = 12345

		# Create grid of original perlin noise.
		self.grid = pn.PerlinNoise(self.shape, self.scale, self.f, self.l, self.a,
								self.p, self.o, self.rand, self.seed)

	def tearDown(self):
		''' No Teardown needed for this test. '''
		pass

	def test_original_perm(self):
		''' Testing Perlin's original permutation... '''
		ogCopy = pn.PerlinNoise(self.shape, self.scale, self.f, self.l, self.a,
								self.p, self.o, self.rand, self.seed)
		# Test shape is same.
		self.assertEqual(self.grid.shape, ogCopy.shape)
		# Test array values are the same.
		self.assertTrue(np.array_equal(self.grid, ogCopy))

	def test_rand_perm(self):
		''' Testing random permutations... '''
		rndCopy = pn.PerlinNoise(self.shape, self.scale, self.f, self.l, self.a,
								self.p, self.o, True, self.seed)

		self.assertFalse(np.array_equal(self.grid, rndCopy))


	def test_rand_seed(self):
		''' Testing Random Permutations with seeds... '''
		rnd1 = pn.PerlinNoise(self.shape, self.scale, self.f, self.l, self.a,
								self.p, self.o, True, self.seed)
		rnd2 = pn.PerlinNoise(self.shape, self.scale, self.f, self.l, self.a,
								self.p, self.o, True, self.seed)
		self.assertTrue(np.array_equal(rnd1, rnd2))


if __name__ == "__main__":
	unittest.main(verbosity=2)