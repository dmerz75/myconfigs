import pandas as pd
import numpy as np
from IPython import get_ipython
from IPython.core.interactiveshell import InteractiveShell

print("Loading 00-startup.py")

# Pandas options
pd.options.display.max_columns = 30
pd.options.display.max_rows = 20

x000 = np.linspace(0, 10, 11)

ipython = get_ipython()

# If in ipython, load autoreload extension
if 'ipython' in globals():
    print('\nWelcome to IPython!')
    try:
        ipython.magic('load_ext autoreload')
        ipython.magic('autoreload 2')
    except AttributeError:
        print("no ipython magic")

# Display all cell outputs in notebook
InteractiveShell.ast_node_interactivity = 'all'

# Visualization
# import plotly.plotly as py
# import plotly.graph_objs as go
# from plotly.offline import iplot, init_notebook_mode
# init_notebook_mode(connected=True)
# import cufflinks as cf
# cf.go_offline(connected=True)
# cf.set_config_file(theme='pearl')

print('Your favorite libraries have been loaded.')