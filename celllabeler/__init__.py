import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter 
import os,sys
import subprocess
import celllabeler
# from ipywidgets import *
# from IPython.display import display
# from IPython.html import widgets

def display_img(img):
	# for _,row in df.iterrows():
	# 	pass

	if '__IPYTHON__':
		from IPython import get_ipython
		ipython = get_ipython()
		ipython.run_line_magic('gui','tk')
	# result = os.system("python celllabeler.py {img}")
	# return result
	# # else:
	root = tkinter.Tk()
	app = App(root,img)
	# # root.mainloop()

	# root.quit()
	# result = subprocess.check_output(["echo","Hello World"])
	
	# result = subprocess.check_output(["python","/Users/lukefunk/packages/celllabeler/celllabeler/celllabeler.py"],stderr=subprocess.STDOUT)
	# return result

class App:

	def __init__(self, master,img):

		frame = tkinter.Frame(master)
		frame.pack()

		self.button = tkinter.Button(
		    frame, text="QUIT", fg="red", command=master.destroy
		    )
		self.button.pack(side=tkinter.LEFT)

		fig = plt.figure(figsize=(10, 10))
		fig.add_subplot(111).imshow(img)

		canvas = FigureCanvasTkAgg(fig,master=frame)  # A tk.DrawingArea.
		canvas.draw()
		canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
