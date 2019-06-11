import pandas as pd
import ops.io
from ops.utils import regionprops,subimage
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
# import celllabeler

def start_gui(df):
	root = tk.Tk()
	app = celllabeler_gui(root,df)
	root.mainloop()

class celllabeler_gui:

	def __init__(self, master,df):
		self.label_iterate = iter(zip(df.label.tolist(),df.img_file.tolist(),df.label_file.tolist()))

		self.frame = tk.Frame(master)
		self.frame.pack()

		self.button_var = tk.IntVar()
		self.button_var.set(0)

		self.display_text = tk.Label(master,textvariable=self.button_var)
		self.display_text.pack()

		self.quit_button = tk.Button(
		    self.frame, text="QUIT", fg="red", command=master.destroy
		    )
		self.quit_button.pack(side=tk.LEFT)

		self.next_button = tk.Button(self.frame,text="NEXT",command=self.next_subimage)
		self.next_button.pack(side=tk.BOTTOM)

		self.fig_setup(self.get_next_subimage())


	def add_one(self):
		self.button_var.set(self.button_var.get()+1)

	def fig_setup(self,first_subimage):
		self.add_one()
		channels = first_subimage.shape[0]
		self.fig,self.subplots = plt.subplots(1,channels,figsize=(5,5))
		self.canvas = FigureCanvasTkAgg(self.fig,master=self.frame)  # A tk.DrawingArea.
		self.canvas.draw()
		self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
		self.display_subimage(first_subimage)

	def get_next_subimage(self):
		label,img_file,labels_file = next(self.label_iterate)
		img = ops.io.read_stack(img_file)

		#max z-project
		if len(img.shape)==4:
			img = img.max(axis=0)
		elif len(img.shape)>4:
			assert Exception('too many image dimensions')

		img_labels = ops.io.read_stack(labels_file)

		regions = regionprops(img_labels,img)

		region = regions[label-1].bbox

		return subimage(img,region,pad=10)

	def next_subimage(self):
	    subimage = self.get_next_subimage()
	    self.display_subimage(subimage)
	    self.add_one()
	    
	def display_subimage(self,img):
		channels = img.shape[0]
		for channel,subplot in zip(range(channels),self.subplots):
			subplot.clear()
			subplot.imshow(img[channel])
			self.canvas.draw()