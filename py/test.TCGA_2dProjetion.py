#!/usr/bin/env python
# coding: utf-8

import sys  
sys.path.insert(0, '../py')
from graviti import *

from numpy.linalg import norm
import numpy as np
import os
import os.path
from os import path
import sys
import glob
import h5py
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # to not display figure while using ssh 
import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.express as px
import hdbscan
import pandas as pd
import umap
import networkx as nx
from scipy import sparse, linalg
import pickle
from sklearn.preprocessing import normalize, scale
from sklearn.decomposition import PCA
from scipy.sparse import find
from numpy.linalg import norm
import timeit
import multiprocessing
from joblib import Parallel, delayed
from datetime import datetime
from tqdm import tqdm

from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly.express as px
import plotly

import warnings
warnings.filterwarnings('ignore')

samples = glob.glob('../BRCA_covds_wo_intensity/*.freq10.covdNN50.features.pkl')

#####################################################################################
# The barycenters array contain the list of covd-barycenters, one per sample
num_cores = multiprocessing.cpu_count() # numb of cores
barycenter_list = Parallel(n_jobs=num_cores)(
    delayed(load_barycenters)(sample) for sample in tqdm(samples) # load_barycenters evaluate the barycenter of the sample
    )

barycenters = np.zeros((len(samples),pd.read_pickle(samples[0])['descriptor'].iloc[0].shape[0]))
row = 0
for b in barycenter_list:
    barycenters[row,:] = b
    row += 1
barycenters = barycenters[~np.all(barycenters == 0, axis=1)]
#######################################################################
# # Load the covd-barycenters for all samples
# outfile = 'covd_barycenters.npy'
# barycenters = np.load(outfile)

cancer_type = []
sample_id = []
for sample in samples:
    cancer_type.append( sample.split('/')[5] )
    sample_id.append( os.path.basename(sample).split('.')[0] )

print(len(cancer_type),set(cancer_type))

# UMAP representations

reducer = umap.UMAP(n_components=2)
embedding = reducer.fit_transform(barycenters)

x = embedding[:,0]
y = embedding[:,1]

df = pd.DataFrame(dict(x=x, y=y, label=cancer_type, sample=sample_id))
groups = df.groupby('label')
# Plot
fig, ax = plt.subplots(figsize=(10,10))
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=3, label=name, alpha=0.75)
#ax.legend()
plt.title('UMAP projection of the BRCA dataset', fontsize=12)
filename = 'umap.BRCA_wo_intensity.s'+str(df.shape[0])+'.pdf'
plt.savefig(filename)

# # In[42]: PCA representations

# pca = PCA(n_components=2)
# principalComponents = pca.fit_transform(barycenters)

# x = principalComponents[:,0]
# y = principalComponents[:,1]

# df = pd.DataFrame(dict(x=x, y=y, label=cancer_type, sample=sample_id))
# groups = df.groupby('label')
# # Plot
# fig, ax = plt.subplots(figsize=(10,10))
# ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
# for name, group in groups:
#     ax.plot(group.x, group.y, marker='o', linestyle='', ms=3, label=name, alpha=0.75)
# ax.legend()
# plt.title('PCA projection of the TCGA dataset', fontsize=12)
# filename = 'pca.s'+str(df.shape[0])+'.pdf'
# plt.savefig(filename)





