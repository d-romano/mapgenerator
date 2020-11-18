# Takes a 2-D array of float values, converts them into a 2D array of rgb values.
from PIL import Image
import numpy as np
import datetime
import math
import os

def writeImg(w, h, heightData, fType='png'):
	img = np.zeros([h,w,3], dtype=np.int8)
	for row in range(h):
		for col in range(w):	 
			r,g,b = floatToRGB(heightData[row][col])
			# Replace with side values for grey-scale.
			img[row][col][0] =  r 	#(r*.299) + (g*.587) + (b * .114)
			img[row][col][1] = g    #(r*.299) + (g*.587) + (b * .114)
			img[row][col][2] = b 	#(r*.299) + (g*.587) + (b * .114)

	# Make directory for saved maps if one doesn't exist.
	if not os.path.exists('my_maps'):
		os.makedirs('my_maps')

	pil_im  = Image.fromarray(img, 'RGB')
	
	imgPath = "./my_maps/map_{}.{}".format(datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S"), fType)


	pil_im.save(imgPath)

	return imgPath


def rgbToHex(rgb):
	''' Convert RGB color tuple to hexidecimal w/ bitshifting. '''
	hexCol = 0
	for col in rgb:
		hexCol = hexCol<< 8
		hexCol = hexCol | col	
	
	return "#" + str(hex(hexCol))[2:]


def floatToRGB(val,  outType='rgb'):
	# Color blending courtesy of https://meyerweb.com/eric/tools/color-blend/
	colorDict = {
		# Water 
		0:(23, 42, 69),				# Navy
		1:(37, 67, 115),			# dark blue
		2:(75, 128, 214),			# light blue
		3:(94,135,200),
		4:(112,141,187),
		5:(131,148,173),			# Blend water + sand
		# Dry Land
		6:(186, 167, 132),			# tan/sand
		7:(159,165,114),			# Dirt
		8:(146,164,105),
		9:(132, 163, 96),			# Light Green
		10:(93,128,78),				# Blend ligh + dark
		11:(74,110,69),
		12:(54, 92, 59),			# dark green
		# Cliffs / Mountains
		13:(107, 110, 85),
		14:(120,123,100),#(77,87,73),			# Start Stone
		15:(133,135,115),#(106,108,106),			# Green to stone
		16:(146,148,131),#(117,119,117),			# Dark grey to add more definintion
		17:(159,161,146),#(129, 130, 129),			# grey/stone
		18:(172,174,161),#(143,144,143),			# light-grey
		19:(185,186,176),#(183,185,183),			# white-grey
		20:(198,199,191),#(172,173,172),			# Blend grey + white
		21:(211,212,207),#(194,194,194), 
		22:(224,224,222),#(215,216,215),
		23:(237,237,237) 			
	}

	# Mid point of current scale
	nColors = len(colorDict) 
	
	mid = (nColors) // 2
	
	# 2 Stems from 
	step = (2 / (nColors-1))
	
	colInd = 0

	if val < 0:
		if val < -1: val = -1
		colInd = (mid) + val // step
	else:
		# Attempt to resolve issues from heightvalues that are way too large.
		if val > 1: val = 1 - ((val/math.floor(val))-1)*.50
		colInd = mid +(val // step)

	if outType == 'rgb':
		return colorDict[colInd]
	else:
		return rgbToHex(colorDict[colInd])