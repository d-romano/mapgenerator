import os
import tkinter as tk
import tkinter.ttk as ttk
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

class DSFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()


	def initWidgets(self):
		''' Initialize widgets with starting info. '''

		self.roughScale = tk.Scale(self, label="Roughness", from_=0, to=4, tickinterval=.5, orient=tk.HORIZONTAL, length=200)
		self.noiseLbl = tk.Label(self, text='Reduce Noise')
		self.noiseVar = tk.IntVar()
		self.noiseChk = tk.Checkbutton(self, variable = self.noiseVar)

	def getNoiseVal(self):
		return self.noiseVar.get()
		# Diamond-Square needs: size, roughness, noise

	def genGrid(self, size, seed):
		return ds.DiamondSquare(size, self.roughScale.get(), seed, self.noiseVar.get())

	def placeWidgets(self):
		''' Add widgets to frame. '''
		self.roughScale.pack()
		self.noiseLbl.pack()
		self.noiseChk.pack()

class PNFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()

	def initWidgets(self):
		self.zoomScale = tk.Scale(self, label="Scale", from_=1, to=10, tickinterval = 1, orient=tk.HORIZONTAL, length=400)
		self.freqScale = tk.Scale(self, label="Frequency", from_=1, to=10, tickinterval=1, orient=tk.HORIZONTAL, length=400)
		self.freqScale.set(10)
		self.lancScale = tk.Scale(self, label="Lancularity", from_=float(0.25), to=float(4.0), tickinterval=float(0.5), resolution=.5, orient=tk.HORIZONTAL, length=400)

		self.ampScale = tk.Scale(self, label="Aplitude", from_=0, to=50, tickinterval=5, orient=tk.HORIZONTAL, length=400)
		self.ampScale.set(10.0)
		self.persScale = tk.Scale(self, label="Persistence", from_=float(0.1), to=float(1.0), tickinterval=float(0.1), resolution=-.1, orient=tk.HORIZONTAL, length=400)
	
		self.octScale = tk.Scale(self, label="Octaves", from_=0, to=8, tickinterval=1, orient=tk.HORIZONTAL, length=400)
		self.octScale.set(4)

		self.randLabel = tk.Label(self, text='Use Random Perm Table')
		self.randVar = tk.IntVar()
		self.randCheck = tk.Checkbutton(self, variable = self.randVar)

	def placeWidgets(self):
		self.zoomScale.pack()
		self.freqScale.pack()
		self.lancScale.pack()
		self.ampScale.pack()
		self.persScale.pack()
		self.octScale.pack()
		self.randLabel.pack(side='left')
		self.randCheck.pack()

	def genGrid(self, size, seed):
		s = self.zoomScale.get()
		f = self.freqScale.get()
		l = float(self.lancScale.get())
		a = self.ampScale.get()
		p = float(self.persScale.get())
		o = self.octScale.get()
		rand = self.randVar.get()
		size = 2**size 
		return pn.PerlinNoise((size,size), s, f, l, a, p ,o, rand)

class optionFrame(tk.Frame):
	''' Frame that holds options for generation and 2 separate option frames '''
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()


	def initWidgets(self):
		# Choose generation algorithm
		self.algoDict = {"Diamond Square":"DSFrame", "Perlin Noise":"PNFrame"}
		self.algoLabel = tk.Label(self, text="Current Generation Algorithm")
		algoVar = tk.StringVar(self)
		algoVar.set("Perlin Noise")
		self.algoChoice = tk.OptionMenu(self, algoVar, *self.algoDict, command=self.getDetailFrame)
		# For size and seed.
		self.sizeScale = tk.Scale(self, label="Map Size", from_=8, to = 10, orient=tk.HORIZONTAL, length=200)
		self.seedLabel = tk.Label(self, text="Seed Value")
		self.seedEntry = tk.Entry(self, width=25)

		self.curFrame = None
		self.detailContainer = tk.Frame(self)
		# Add frames to container
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
		return self.sizeScale.get()

	def genGrid(self):
		return self.curFrame.genGrid(self.getSize(), self.seedEntry.get())	

	def placeWidgets(self):
		self.algoLabel.grid(row=0, column=0)
		self.algoChoice.grid(row=1, column=0, sticky='ew')
		self.sizeScale.grid(row=2, column=0)
		self.seedLabel.grid(row=3, column=0)
		self.seedEntry.grid(row=4, column=0)
		self.detailContainer.grid(row=5, column=0)


class mapCanvasFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()

	def initWidgets(self):
		self.mapCanvas = tk.Canvas(self, width=256, height = 256, bg="#808080")

	def placeWidgets(self):
		self.mapCanvas.pack(side="top", fill="both", expand=True)

	def getCanvas(self):
		return self.mapCanvas

	def setCanvas(self, canvas):
		self.mapCanvas = mapCanvasFrame()


class GeneratorFrame(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.initWidgets()
		self.placeWidgets()

	def initWidgets(self):
		#display = tk.Frame(self).pack()
		self.mapFrame = mapCanvasFrame(parent=self,controller=None)
		self.options = optionFrame(parent=self,controller=None)
		self.genButton = tk.Button(self, text="Generate", command=self.genMap)

	def placeWidgets(self):
		self.mapFrame.grid(row = 0, column = 0, columnspan=2)
		self.options.grid(row = 0, column = 3)
		self.genButton.grid(row = 1, column = 3)

	def genMap(self):
		
		pxSize = (2**self.options.getSize())
		grid = self.options.genGrid()

		img = tk.PhotoImage(width=pxSize, height=pxSize)

		mapCanvas = self.mapFrame.getCanvas()
		mapCanvas['width'] = pxSize
		mapCanvas['height'] = pxSize
		mapCanvas.create_image((pxSize//2, pxSize//2), image=img, state='normal')


		for x in range(pxSize):
			for y in range(pxSize):
				color = WriteImage.floatToRGB(grid[y][x], 'hex')
				img.put(color, (x,y))

		tk.mainloop()


class mainApp(tk.Tk):
	''' Main application that controls which frames are being displayed.'''
	# https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		# Dictionary that holds all needed frames in the application.

		container = tk.Frame(self)
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
	#root = tk.Tk()
	app = mainApp()
	# Create application running loop.
	app.mainloop()
