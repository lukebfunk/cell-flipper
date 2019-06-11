# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import tkinter as tk
# import os,sys
# import subprocess
# import celllabeler
# # from ipywidgets import *
# # from IPython.display import display
# # from IPython.html import widgets

# def test():


# 	class MyApp:

# 	    def __init__(self, root):
# 	        frame = tk.Frame(root)
# 	        frame.pack()

# 	        self.button = tk.Button(frame, text="Hello", command=self.hello_world)
# 	        self.button.pack(side=tk.LEFT)

# 	        self.quitbutton = tk.Button(frame, text="QUIT", fg="red", command=root.destroy)
# 	        self.quitbutton.pack(side=tk.RIGHT)

# 	    def hello_world(self):
# 	        print("Hello World!")

# 	root = tk.Tk()

# 	app = MyApp(root)


# def display_img(img):
# 	# for _,row in df.iterrows():
# 	# 	pass

# 	# if '__IPYTHON__':
# 	# 	from IPython import get_ipython
# 	# 	ipython = get_ipython()
# 	# 	ipython.run_line_magic('gui','tk')
# 	# result = os.system("python celllabeler.py {img}")
# 	# return result
# 	# # else:
# 	class App:

# 		def __init__(self, master,img):

# 			frame = tk.Frame(master)
# 			frame.pack()

# 			self.button = tk.Button(
# 			    frame, text="QUIT", fg="red", command=master.destroy
# 			    )
# 			self.button.pack(side=tk.LEFT)


# 			fig = plt.figure(figsize=(10, 10))
# 			fig.add_subplot(111).imshow(img)

# 			canvas = FigureCanvasTkAgg(fig,master=frame)  # A tk.DrawingArea.
# 			canvas.draw()
# 			canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 	root = tk.Tk()
# 	app = App(root,img)

# 	# try:
# 	import IPython.lib.inputhook as ih
# 	ih.TkInputHook(ih.InputHookManager).enable(root)
# 	# except ImportError:
# 	#     root.mainloop()

# 	# # root.mainloop()

# 	# root.quit()
# 	# result = subprocess.check_output(["echo","Hello World"])
	
# 	# result = subprocess.check_output(["python","/Users/lukefunk/packages/celllabeler/celllabeler/celllabeler.py"],stderr=subprocess.STDOUT)
# 	# return result

