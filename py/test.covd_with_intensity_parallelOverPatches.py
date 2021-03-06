#!/usr/bin/env python
# coding: utf-8
import sys
sys.path.insert(0, '../py')
from graviti import * # load the local gravity module containing the "process_patch_with_intensity" function

import numpy as np
import scipy as sp
from scipy.sparse import coo_matrix

from skimage.draw import polygon
from skimage import io
from skimage.measure import label, regionprops
import skimage.io
import skimage.measure
import skimage.color

import glob
import pandas as pd
import os
import timeit
import random

from matplotlib import pyplot as plt
import matplotlib.patches as mpatches

import timeit
import multiprocessing
from joblib import Parallel, delayed
from datetime import datetime
from tqdm import tqdm

sample_id = sys.argv[1] # get the sample id

if len(sys.argv) == 3:
    svs_filename = sys.argv[2];
    print( os.path.basename(svs_filename) )

patches = glob.glob(sample_id+'/*_polygon/*/*.csv') # this matches the directory structure of the dataset and return the list of patches in the sample

# Process in parallel the patches in the sample
num_cores = multiprocessing.cpu_count() # numb of cores

# fraction of nuclei in the patch to be processed hardcoded to 1 (=all)
generated_covds = Parallel(n_jobs=num_cores)( delayed(process_patch_with_intensity)(p,1,svs_filename) for p in tqdm(patches) )

