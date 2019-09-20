import pandas as pd
from ops.io import read_stack as read
from ops.io import ij_open
from ops.utils import regionprops,subimage
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from functools import partial
from ops.io_hdf import read_hdf_image

#TODO
# reduce ops dependencies
# return uncompleted table if quit before finishing
# save final table to daughter directory, not current directory
# handle finishing final iteration through cells
# go back in case of mis-click
# GUI preference selection
# Fiji integration?

#FIJI-esque LUTs
ramp = list(range(256))
ZERO = [0]*256
ONE = [255]*256
PLT_RED     = np.stack([ramp,ZERO,ZERO,ONE],axis=1)/255
PLT_GREEN   = np.stack([ZERO,ramp,ZERO,ONE],axis=1)/255
PLT_BLUE    = np.stack([ZERO,ZERO,ramp,ONE],axis=1)/255
PLT_MAGENTA = np.stack([ramp,ZERO,ramp,ONE],axis=1)/255
PLT_GRAY    = np.stack([ramp,ramp,ramp,ONE],axis=1)/255
PLT_CYAN    = np.stack([ZERO,ramp,ramp,ONE],axis=1)/255

DEFAULT_PLT_LUTS = PLT_GRAY, PLT_GREEN, PLT_RED, PLT_MAGENTA, PLT_CYAN, PLT_GRAY, PLT_GRAY
DEFAULT_PLT_LUTS = list(map(ListedColormap,DEFAULT_PLT_LUTS))


def start_CellFlipper(df):
	root = tk.Tk()
	app = CellFlipper(root,df)
	root.mainloop()
	cell_classification = app.cell_classification
	root.destroy()
	df_result = (df
				 .head(len(cell_classification))
				 .assign(flipper_class=cell_classification)
				)
	read.keys['active'] = False
	return df_result

class CellFlipper:

	def __init__(self, master,df,classes=['interphase','mitotic'],mode='plt'):
		self.mode=mode

		# self.label_iterate = iter(zip(df.label.tolist(),df.img_file.tolist(),df.label_file.tolist()))
		self.label_iterate = iter(zip(df.label.tolist(),df.img_file.tolist(),df.bounds.tolist()))

		frame = tk.Frame(master)
		frame.grid(row=0,column=0) #use grid for master

		self.cell_classification = []

		self.button_var = tk.IntVar()
		self.button_var.set(0)

		display_current = tk.Label(master,textvariable=self.button_var)
		display_current.grid(row=0,column=1)

		display_total = tk.Label(master,text=' of '+str(df.pipe(len)))
		display_total.grid(row=0,column=2)

		quit_button = tk.Button(
		    master, text="QUIT", fg="red", command=master.quit
		    )
		quit_button.grid(row=1,column=1)

		master.protocol("WM_DELETE_WINDOW", master.quit)

		read.keys['active'] = True

		self.fig_setup(frame,self.get_next_subimage())

		class_buttons = [tk.Button(frame,text=label_class+' [{}]'.format(order+1),command=partial(self.next_subimage,label_class)) 
							for order,label_class in enumerate(classes)]

		for num,(button,label_class) in enumerate(zip(class_buttons,classes)):
			button.pack(side=tk.TOP) #use pack for frame
			master.bind(str(num+1),partial(self.next_subimage,label_class))


	def fig_setup(self,frame,first_subimage):
		self.add_one()
		if self.mode != 'fiji':
			channels = first_subimage.shape[0]
			self.fig,self.subplots = plt.subplots(1,channels,figsize=(10,5))
			self.canvas = FigureCanvasTkAgg(self.fig,master=frame)  # A tk.DrawingArea.
			self.canvas.draw()
			self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1) #use pack for frame
		self.display_subimage(first_subimage)

	def next_subimage(self,classification,_event=None):
		self.cell_classification.append(classification)
		self.display_subimage(self.get_next_subimage())
		self.add_one()

	def get_next_subimage(self):
		# label,img_file,labels_file = next(self.label_iterate)
		label,img_file,bounds = next(self.label_iterate)

		if img_file.endswith('tif'):
			img = read(img_file)
			# img_labels = read(labels_file)
			# regions = regionprops(img_labels,img)
			# region = regions[label-1].bbox
			img_sub = subimage(img,bounds,pad=10)
		elif img_file.endswith('hdf'):
			bounds = np.array(bounds) + np.array([-10, -10, 10, 10])
			img_sub = read_hdf_image(img_file,bbox=bounds)
		#max z-project
		if len(img_sub.shape)==4:
			img_sub = img_sub.max(axis=0)
		elif len(img_sub.shape)>4:
			assert Exception('too many image dimensions')

		return img_sub

	def display_subimage(self,img):
		if self.mode =='fiji':
			ij_open(img)
			# adjust fiji window size
			# close window
		else:
			channels = img.shape[0]
			for channel,subplot,cmap in zip(range(channels),self.subplots,DEFAULT_PLT_LUTS[:channels]):
				subplot.clear()
				subplot.imshow(img[channel],cmap=cmap)
				self.canvas.draw()

	def add_one(self):
		self.button_var.set(self.button_var.get()+1)
