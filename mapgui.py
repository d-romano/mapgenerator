import os
import math
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk

from PIL import ImageTk, Image

from diamondsquare import DiamondSquare as ds
from perlin import Perlin as pn
from writeimage import WriteImage

dir_path = os.path.dirname(os.path.realpath(__file__))


''' Three two types of pages needed:
	1.) Intro / Welcome page explaining what app does
	2.) Creation page
			- Algo option section
			   > Frame for perlin noise
			   > Frame for diamond square
			- Image Generation section
'''

class ScaleFrame(Frame):
	def __init__(self, parent, controller, varType, to, from_, name):
		Frame.__init__(self, parent)
		self.initWidgets(varType, to, from_, name)

	def initWidgets(self, varType, to, from_, name):
		nameLbl = Label(self, text=name).grid(row = 0, column = 0, pady=(10,0), columnspan=2, sticky=W)
		self.var = varType()
		self.var.set(from_)
		# Used for validating input.
		vcmd = (self.register(self.validateEntry), '%P', to, from_)
		self.varEntry = Entry(self, textvariable=self.var, validate='focusout', width = 4, validatecommand=vcmd)
		self.scale = Scale(self, from_=from_, to=to, orient=HORIZONTAL, length=400, variable=self.var, command=self.roundVal)
		self.scale.grid(row = 1, column = 0, columnspan=3, pady=(0,10))
		self.varEntry.grid(row=1, column=4)

	def validateEntry(self, editedVal, to, from_):
		try:
			# Validate an integer input
			 valid = int(from_) <= int(editedVal) <= int(to)
			 if not valid:
			 	if int(editedVal) < int(from_):
			 		self.var.set(from_)
			 	else:
			 		self.var.set(to)
		except ValueError:
			# If not integer attempt to validate float
			try:
				valid = float(from_) <= float(editedVal) <= float(to) 
				if valid:
					self.roundVal(float(editedVal))
				if not valid:
				 	if  float(editedVal) < float(from_):
				 		self.var.set(float(from_))
				 	else:
				 		self.var.set(float(to))

			except ValueError:
				# If Text entry is empty then set to lowest val
				if not editedVal:
					self.var.set(from_)
				# Or return false, cannot validate strings
				return False
		# Validaiton passed.
		return True

	def roundVal(self, val):
		# Esnures there are no random floats in the label
		self.var.set(round(self.var.get(),2))

	def getVal(self):
		return self.var.get()


class DSFrame(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()


	def initWidgets(self):
		''' Initialize widgets with starting info. '''

		self.roughScale = ScaleFrame(self, None, from_=0, to=4, varType=IntVar, name="Roughness")
		self.noiseLbl = Label(self, text='Reduce Noise')
		self.noiseVar = IntVar()
		self.noiseChk = Checkbutton(self, variable = self.noiseVar)

	def getNoiseVal(self):
		return self.noiseVar.get()
		# Diamond-Square needs: size, roughness, noise

	def genGrid(self, size, seed):
		return ds.DiamondSquare(size, self.roughScale.getVal(), seed, self.noiseVar.get())

	def placeWidgets(self):
		''' Add widgets to frame. '''
		self.roughScale.pack()
		self.noiseLbl.pack()
		self.noiseChk.pack()


class PNFrame(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()

	def initWidgets(self):
		self.zoomScale = ScaleFrame(self, None, from_=1, to=10, varType=IntVar, name="Zoom")
		self.freqScale = ScaleFrame(self, None, from_=1, to=10, varType=IntVar, name="Frequency")	
		self.lancScale = ScaleFrame(self, None, from_=.25, to=4, varType=DoubleVar, name="Lancularity") 
		self.ampScale = ScaleFrame(self, None, from_=0, to=50, varType=IntVar, name="Amplitude")
		self.persScale = ScaleFrame(self, None, from_=.1, to=1.0, varType=DoubleVar, name="Persistence")
		self.octScale = ScaleFrame(self, None, from_=1, to=8, varType=IntVar, name="Octaves")
		
		self.randLbl = Label(self, text='Use Random Perm Table')
		self.randVar = IntVar()
		self.randCheck = Checkbutton(self, variable = self.randVar)

	def placeWidgets(self):
		self.zoomScale.pack()
		self.freqScale.pack()
		self.lancScale.pack()
		self.ampScale.pack()
		self.persScale.pack()
		self.octScale.pack()
		self.randLbl.pack(side='left', padx=(0, 10))
		self.randCheck.pack(anchor=W)

	def genGrid(self, size, seed):
		s = self.zoomScale.var.get()
		f = self.freqScale.getVal()
		l = float(self.lancScale.getVal())
		a = self.ampScale.getVal()
		p = float(self.persScale.getVal())
		o = self.octScale.getVal()
		rand = self.randVar.get()
		return pn.PerlinNoise(size, s, f, l, a, p ,o, rand, seed)


class optionFrame(Frame):
	''' Frame that holds options for generation and 2 separate option frames '''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		
		self.initWidgets()
		self.placeWidgets()


	def initWidgets(self):
		# Choose generation algorithm
		self.algoDict = {"Diamond Square":"DSFrame", "Perlin Noise":"PNFrame"}
		self.algoLabel = Label(self, text="Current Generation Algorithm")
		algoVar = StringVar(self)
		self.algoChoice = OptionMenu(self, algoVar, self.algoDict["Perlin Noise"], *self.algoDict, command=self.getDetailFrame)
		
		# For size and seed.
		self.sizeScale = ScaleFrame(self, None, from_=8, to=10, varType=IntVar, name="Size")
		self.seedLabel = Label(self, text="Seed Value")
		self.seedEntry = Entry(self, width=25)

		# For holding the frames with generation options.
		self.curFrame = None
		self.detailContainer = Frame(self)
		# Add frames to container to allow changing between active frames
		self.frames = {}
		for F in (DSFrame, PNFrame):
			page_name = F.__name__
			self.curFrame = F(parent=self.detailContainer, controller=self)
			self.frames[page_name] = self.curFrame
			self.curFrame.grid(row=0, column=0, sticky="nsew")

	def getDetailFrame(self, fName):
		self.curFrame = self.frames[self.algoDict[fName]]
		self.curFrame.tkraise()

	def getSize(self):
		return self.sizeScale.getVal()

	def getSeed(self):
		seed = self.seedEntry.get()
		try:
			seed = int(seed)
		except:
			try:
				temp = 0
				for char in seed:
					temp += int(ord(char))
				seed = temp
			except:
				seed = None
		return seed

	def genGrid(self):
		return self.curFrame.genGrid(self.getSize(), self.getSeed())	

	def placeWidgets(self):
		self.algoLabel.grid(row=0, column=0, sticky=W)
		self.algoChoice.grid(row=1, column=0, sticky='ew')
		self.sizeScale.grid(row=2, column=0)
		self.seedLabel.grid(row=3, column=0)
		self.seedEntry.grid(row=4, column=0)
		self.detailContainer.grid(row=5, column=0)


class mapCanvasFrame(Frame):
	''' Frame holds map canvas. '''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()

	def initWidgets(self):
		self.mapCanvas = Canvas(self, width = 256, height = 256, bg="#808080")

	def placeWidgets(self):
		self.mapCanvas.pack(side="top", fill="both", expand=True)

	def getCanvas(self):
		return self.mapCanvas

	def setCanvas(self, canvas):
		self.mapCanvas = mapCanvasFrame()


class GeneratorFrame(Frame):
	''' Main Frame to display the generation options. '''
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		# Controller is the main app window.
		self.controller = controller
		self.initWidgets()
		self.placeWidgets()

	def initWidgets(self):
		#display = Frame(self).pack()
		self.mapFrame = mapCanvasFrame(parent=self,controller=None)
		self.options = optionFrame(parent=self,controller=None)
		self.options.config(relief=SUNKEN, borderwidth=1, padding=(50, 25, 50,25))
		self.genButton = Button(self, text="Generate", command=self.genMap)

	def placeWidgets(self):
		
		self.mapFrame.grid(row = 0, column = 0, columnspan=2, padx=50, pady=50, sticky=W)
		self.options.grid(row = 0, column = 3, pady='.5i', padx='.5i', sticky=E)
		self.genButton.grid(row = 1, column = 3)
		

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Replace with something faster! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	def genMap(self):
		pxSize = (2**self.options.getSize())

		self.controller.geometry(f"{pxSize+750}x{pxSize + 480}")

		grid = self.options.genGrid()

		imgLoc = WriteImage.writeImg(pxSize, pxSize, grid)

		# Load image from temporary location and convert to tk photo
		img = Image.open(imgLoc)
		photo = ImageTk.PhotoImage(img)
		
		# Get the map canvas, clear old images and resize.
		mapCanvas = self.mapFrame.getCanvas()
		mapCanvas.delete('all')
		mapCanvas.config(height=pxSize, width=pxSize)

		# size/2 since tkinter canvas 0,0 starts in center.
		mapCanvas.create_image(pxSize/2, pxSize/2, image=photo)
		

		'''
		img = PhotoImage(width=pxSize, height=pxSize)

		mapCanvas = self.mapFrame.getCanvas()
		mapCanvas['width'] = pxSize
		mapCanvas['height'] = pxSize
		mapCanvas.create_image((pxSize//2, pxSize//2), image=img, state='normal')

		
		for x in range(pxSize):
			for y in range(pxSize):
				color = WriteImage.floatToRGB(grid[y][x], 'hex')
				img.put(color, (x,y))
		'''
		mainloop()


class mainApp(ThemedTk):
	''' Main application that controls which frames are being displayed.'''
	# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
	def __init__(self, *args, **kwargs):
		ThemedTk.__init__(self, *args, **kwargs)
		# Dictionary that holds all needed frames in the application.
		self.geometry("1024x720")
		self.title("Map Generator")

		# Create main menu of the applicaiton
		menubar = Menu(self)
		menubar.add_command(label="Quit", command=self.quit)
		self.config(menu=menubar)

		# Create all the main frames of the application for easy access.
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		self.frames = {}
		for F in (GeneratorFrame,):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=0, column=0, sticky="nsew")



	def getFrame(self, fName):
		''' Get Frame from dictionary and raise. '''
		frame = self.frames[fName]
		frame.tkraise()


if __name__ == '__main__':
	# Create TKinter application
	#root = Tk()
	app = mainApp(theme="ubuntu")
	# Create application running loop.
	app.mainloop()
	print("Done!")