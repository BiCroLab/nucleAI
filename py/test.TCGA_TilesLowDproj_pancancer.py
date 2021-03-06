#!/usr/bin/env python
# coding: utf-8

# Samples random tiles from each WSI, for all tissues together, and project covd to lowD with umap

import sys  
sys.path.insert(0, '../py')
from graviti import *

import numpy as np
import os
import os.path
from os import path
import sys
import glob
import h5py
import pandas as pd
import pickle
import timeit
import multiprocessing
from joblib import Parallel, delayed
from datetime import datetime
from tqdm import tqdm
import umap
import warnings
warnings.filterwarnings('ignore')

sample_size = 100 # the number of tiles to sample from each WSI

all_samples = glob.glob('/media/garner1/hdd2/TCGA_polygons/*/*/*.freq10.covdNN50.features.pkl')
print(len(all_samples))
from random import sample
samples = sample(all_samples,500) # take 1000 random WSI from pan-cancer
print(len(samples))
df_tissue = pd.read_pickle(samples[0]).sample(sample_size) # load the first instance of a WSI
cancer_type = [ samples[0].split('/')[5] for i in range(sample_size) ]
for idx, sample in enumerate(samples[1:]):
    print(idx)
    cancer_type.extend( [sample.split('/')[5] for i in range(sample_size)] )
    df = pd.read_pickle(sample)
    df_tissue = df_tissue.append(df.sample(sample_size))

print('Done with loading, now projecting')

reducer = umap.UMAP(n_components=2)
data = np.array(df_tissue[df_tissue['covd']==1].descriptor.tolist()).real # generate the global array of tiles

# filename = 'df.pancancer.s'+str(df.shape[0])
# df_tissue.to_pickle(filename)
# del(df_tissue) # to make space for parallelization over tissue types
embedding = reducer.fit_transform(data) # reduce to lowD with umap

x = embedding[:,0]
y = embedding[:,1]

df = pd.DataFrame(dict(x=x, y=y, label=cancer_type))
# Plot
groups = df.groupby('label')
# Plot
fig, ax = plt.subplots(figsize=(10,10))
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
for name, group in groups:
    ax.plot(group.x, group.y, marker='o', linestyle='', ms=2, label=name, alpha=0.75)
ax.legend()
plt.title('UMAP projection of pan-cancer tiles', fontsize=12)
filename = 'umap.pancancer.s'+str(df.shape[0])+'.pdf'
plt.savefig(filename)

# fig, ax = plt.subplots(figsize=(10,10))
# ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
# ax.plot(x, y, marker='o', linestyle='', ms=1, alpha=0.75)
# plt.title('UMAP projection of pan-cancer tiles', fontsize=12)
# filename = 'umap.pancancer.s'+str(df.shape[0])+'.pdf'
# plt.savefig(filename)

