import pandas as pd
import celllabeler
import sys

if len(sys.argv) == 1:
	raise Exception('Need table file input')
elif len(sys.argv) > 2:
	raise Exception('only 1 input needed (table file)')

table_file = sys.argv[1]
df = pd.read_hdf(table_file)

celllabeler.start_gui(df)