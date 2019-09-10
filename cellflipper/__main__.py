import pandas as pd
import cellflipper
import sys
import tkinter as tk
from tkinter import filedialog
from os.path import splitext,dirname
from ops.io import read_stack as read
from ops.process import feature_table
from ops.features import features_basic

table_ext = [".csv",".hdf"]
image_ext = [".tif",".tiff"]

if len(sys.argv) == 1:
	root_1 = tk.Tk()
	root_1.withdraw()
	filename_1 = (filedialog
				  .askopenfilename(initialdir="/",
				  				   title="Select table (.csv or .hdf) or labeled image (.tif)",
				  				   filetypes=(("table files",("*.csv","*.hdf")),
				  				   			  ("image files","*.tif"),
				  				   			  ("all files","*.*")
				  				   			 )
				  				  )
				 )
	root_1.destroy()

	_,ext_1= splitext(filename_1)

	if ext_1 in table_ext:
		table_file = filename_1
		df = pd.read_hdf(table_file)

	elif ext_1 in image_ext:
		label_file = filename_1
		root_2 = tk.Tk()
		root_2.withdraw()
		filename_2 = (filedialog
				  	  .askopenfilename(initialdir=dirname(label_file),
				  				   	   title="Select intensity image (.tif)",
				  				   	   filetypes=(("image files","*.tif"),
				  				   	   			  ("all files","*.*")
				  				   	   			 )
				  				  	  )
				 	 )

		root_2.destroy()
		_,ext_2= splitext(filename_2)

		if ext_2 not in image_ext:
			raise Exception('intensity image file must be .tif or .tiff')
		else:
			img_file = filename_2
			img_labels = read(label_file)

			df = (feature_table(img_labels, img_labels, features_basic)
        		  .assign(label_file=label_file,img_file=img_file)
        		 )

	else:
		table_file = filename_1
		raise Exception('input table file must be .csv or .hdf')

elif len(sys.argv) == 2:
	filename_1 = sys.argv[1]
	_,ext_1= splitext(filename_1)
	if ext_1 not in table_ext:
		raise Exception('input table file must be .csv or .hdf')
	else:
		table_file = filename_1
		df = pd.read_hdf(table_file)
elif len(sys.argv) > 2:
	raise Exception('only 1 input needed (table file)')

df_result = cellflipper.start_CellFlipper(df)
df_result.to_hdf('table-classified.hdf',key='hdf')