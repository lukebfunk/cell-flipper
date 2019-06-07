import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
# from ipywidgets import *
# from IPython.display import display
# from IPython.html import widgets

def display_img(img):
	# for _,row in df.iterrows():
	# 	pass
	root = Tk()

	app = App(root)
	root.mainloop()
	root.destroy()

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        fig = Figure(figsize=(10, 10))
		fig.add_subplot(111).imshow(img)

		canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
		canvas.draw()
		canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
