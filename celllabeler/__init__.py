import pandas as pd
from ops.io import read_stack as read
from ops.utils import regionprops,subimage
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from functools import partial

#TODO
# GUI file and preference selection
# Fiji integration


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


def start_gui(df):
	root = tk.Tk()
	app = celllabeler_gui(root,df)
	root.mainloop()
	cell_classification = app.cell_classification
	df_result = (df
				 .head(len(cell_classification))
				 .assign(label_class=cell_classification)
				)
	df_result.to_hdf('table-classified.hdf',key='hdf')

class celllabeler_gui:

	def __init__(self, master,df,classes=['interphase','mitotic']):
		self.label_iterate = iter(zip(df.label.tolist(),df.img_file.tolist(),df.label_file.tolist()))

		frame = tk.Frame(master)
		frame.grid(row=0,column=0)

		self.cell_classification = []

		self.button_var = tk.IntVar()
		self.button_var.set(0)

		display_current = tk.Label(master,textvariable=self.button_var)
		display_current.grid(row=0,column=1)

		display_total = tk.Label(master,text=' of '+str(df.pipe(len)))
		display_total.grid(row=0,column=2)

		quit_button = tk.Button(
		    master, text="QUIT", fg="red", command=master.destroy
		    )
		quit_button.grid(row=1,column=1)

		self.fig_setup(frame,self.get_next_subimage())

		class_buttons = [tk.Button(frame,text=label_class+' [{}]'.format(shortcut+1),command=partial(self.next_subimage,label_class)) 
							for shortcut,label_class in enumerate(classes)]

		for num,button in enumerate(class_buttons):
			button.pack(side=tk.BOTTOM)
			master.bind(str(num+1),partial(self.next_subimage,label_class))


	def fig_setup(self,frame,first_subimage):
		self.add_one()
		channels = first_subimage.shape[0]
		self.fig,self.subplots = plt.subplots(1,channels,figsize=(5,5))
		self.canvas = FigureCanvasTkAgg(self.fig,master=frame)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		self.display_subimage(first_subimage)

	def next_subimage(self,classification,_event=None):
		self.cell_classification.append(classification)
		subimage = self.get_next_subimage()
		self.display_subimage(subimage)
		self.add_one()

	def get_next_subimage(self):
		label,img_file,labels_file = next(self.label_iterate)
		img = read(img_file)

		#max z-project
		if len(img.shape)==4:
			img = img.max(axis=0)
		elif len(img.shape)>4:
			assert Exception('too many image dimensions')

		img_labels = read(labels_file)

		regions = regionprops(img_labels,img)

		region = regions[label-1].bbox

		return subimage(img,region,pad=10)

	def display_subimage(self,img):
		channels = img.shape[0]
		for channel,subplot,cmap in zip(range(channels),self.subplots,DEFAULT_PLT_LUTS[:channels]):
			subplot.clear()
			subplot.imshow(img[channel],cmap=cmap)
			self.canvas.draw()

	def add_one(self):
		self.button_var.set(self.button_var.get()+1)