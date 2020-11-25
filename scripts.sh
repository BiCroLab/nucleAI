#!/usr/bin/env bash

# Edit the directory path containing the svs images for a specific cancer type (in this case LUSC)
# in both for loops

# First generate morphological features per sample
# the output is stored in the data/features dir
step=1 
for svs in `ls /media/garner1/hdd2/svs_LUSC/*/*.svs`; do bash script.intensity.sh $svs $step; done

# Second evaluate the covariance descriptor of the morphological features per sample
# the output is stored in the data/covds dir
step=2 # if doing first or second step in pipeline
for svs in `ls /media/garner1/hdd2/svs_LUSC/*/*.svs`; do bash script.intensity.sh $svs $step; done






