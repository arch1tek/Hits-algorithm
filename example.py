
#%%
import numpy as np
from scipy.linalg import eig

import matplotlib.pyplot as plt
import numpy as np
import timeit
import math
import random
from hits import baseset, hitsscores
import networkx as nx
web_graph = nx.read_gpickle("web_graph.gpickle")

plt.rcParams['figure.figsize'] = [10, 6] # set size of plot

ns = np.linspace(1, 100, 100, dtype=int)
print(ns)
ts = [timeit.timeit('hitsscores(web_graph,resultbase)', 
                    setup='resultbase=[x for x in range({})]'.format(n),
                    globals=globals(),
                    number=1)
      for n in ns]

plt.plot(ns, ts, 'og')
degree = 4
coeffs = np.polyfit(ns, ts, degree)
p = np.poly1d(coeffs)
plt.plot(ns, [p(n) for n in ns], '-b')

#%%