import pandas as pd
import celllabeler
import sys

if len(sys.argv) == 1:
	raise Exception('Need table file input')
elif len(sys.argv) > 2:
	raise Exception('only 1 input needed (table file)')

table_file = sys.argv[1]
df = pd.read_hdf(table_file)

df_result = celllabeler.start_gui(df)
df_result.to_hdf('table-classified.hdf',key='hdf')