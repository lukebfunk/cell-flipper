import pandas as pd
from ops.io import read_stack as read
from ops.utils import regionprops,subimage
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from functools import partial
# import celllabeler

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
		frame.pack()

		self.cell_classification = []

		self.button_var = tk.IntVar()
		self.button_var.set(0)

		display_text = tk.Label(master,textvariable=self.button_var)
		display_text.pack()

		quit_button = tk.Button(
		    frame, text="QUIT", fg="red", command=master.destroy
		    )
		quit_button.pack(side=tk.LEFT)

		class_buttons = [tk.Button(frame,text=label_class,command=partial(self.next_subimage,label_class)) for label_class in classes]

		for button in class_buttons:
			button.pack(side=tk.BOTTOM)

		self.fig_setup(frame,self.get_next_subimage())

	def fig_setup(self,frame,first_subimage):
		self.add_one()
		channels = first_subimage.shape[0]
		self.fig,self.subplots = plt.subplots(1,channels,figsize=(5,5))
		self.canvas = FigureCanvasTkAgg(self.fig,master=frame)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		self.display_subimage(first_subimage)

	def next_subimage(self,classification):
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
		for channel,subplot in zip(range(channels),self.subplots):
			subplot.clear()
			subplot.imshow(img[channel])
			self.canvas.draw()

	def add_one(self):
		self.button_var.set(self.button_var.get()+1)