# Takes a 2-D array of float values, converts them into a 2D array of rgb values.

'''
	PPM format:

	header: 
		MagicNum(P3/P6) W  H maxColorVal \n

		[H][W] raster of RGB triplets

	example:

	P3 4 4 15

	000 000 000 000
	000 000 000 000
	000 000 000 000
	000 000 000 000


	This creates a 4x4 Image of white pixels.
'''

import numpy as np
import datetime
import os


def writeImage(w, h, heightData, maxVal):

	# Create .ppm header using passed information
	header = "P6 {} {} 255\n".format(w, h)

	# Array consisting of 8-bit each triplet is one 24-bit color pixel
	img = np.array([0,0,0]*w*h, dtype=np.int8)


	# Move through entire array, generating terrain color for pixel value and placing in image.
	for row in range(h):
		for col in range(w):

			ind = 3 * (row*w + col) 

			r,g,b = floatToRGB(heightData[row][col], maxVal)

			img[ind] = r
			img[ind+1] = g
			img[ind + 2] = b

	# Make directory for saved maps if one doesn't exist.
	if not os.path.exists('my_maps'):
		os.makedirs('my_maps')

	# Open file with name based on current time/date
	with open('./my_maps/map%s.ppm' % datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S"), 'wb') as f:
		f.write(bytearray(header,'ascii'))
		img.tofile(f)


def floatToRGB(val, maxVal):
	colDict = { 
		0:(23, 42, 69),				# Navy
		1:(37, 67, 115),			# dark blue
		2:(75, 128, 214),			# light blue
		3:(186, 167, 132),			# tan/sand
		4:(132, 163, 96),			# Light Green
		5:(54, 92, 59),				# dark green
		6:(92, 94, 91),				# gray/stone
		7:(182, 184, 182) 			# white
	}



	'''	
	if val < -maxVal:
		return colDict[1]
	elif val <= 0:
		return colDict[3]
	elif val < maxVal:
		return colDict[4]
	else: return colDict[5]
	'''
	
	top = -maxVal
	step = (maxVal / 7) * 2 

	# Return rgb colors for pixels.
	for x in range(6):
		if val <= top:
			return colDict[x]
		top += step

	#print(f"{val} > {maxVal}")
	return colDict[6]


if __name__ == '__main__':
	writeImage(255,255, None, 1)