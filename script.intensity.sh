#!/usr/bin/env bash

# Step #1 of this script generates the morphometric features
# Step #2 of this script generates the covariance descriptors after the features have been generated
# Check that the path to the anaconda folder is correct

svsSample=$1 # the full path to the sample svs file
step=$2     # the first or second step in the pipeline: possible values are 1 or 2

cancer_type=`echo $svsSample | cut -d '/' -f5|cut -d '_' -f2` # get the cancer type
samplename=`echo $svsSample | cut -d '/' -f7 | cut -d'.' -f1` # get the sample name

# Check that the locations of the polygons generated by the segmentation process is correct
# Edit the directory location if necessary:
polygons='/media/garner1/hdd2/TCGA_polygons/'$cancer_type'/'$samplename'.*.tar.gz/'$samplename'.*.tar.gz'
dirSample='/media/garner1/hdd2/TCGA_polygons/'$cancer_type'/'$samplename'.*.tar.gz'

echo ${cancer_type} ${samplename}

if [ $step == 1 ]; then
    if test -d $dirSample; then
	echo "Uncompress"
	cd $dirSample
	tar -xf *.gz -C $PWD

	echo "Generate the intensity features"
	cp $svsSample ~/local.svs # cp the sample to a file stored on the fast ssd memory
	rm -f ${dirSample}/*_polygon/${samplename}.*/*.pkl # clean the directory
	# Process in parallel the patches in the sample
	# the output is stored in the data/features directory
	/usr/local/share/anaconda3/bin/ipython ./py/test.covd_with_intensity_parallelOverPatches.py $dirSample ~/local.svs

	# The output features are stored as pkl files in ./data/features directory
	mkdir -p ./data/features/${cancer_type}/${samplename}
	mv ${dirSample}/*_polygon/${samplename}.*/*.pkl ./data/features/${cancer_type}/${samplename}

	echo "Clean up"
	rm ~/local.svs
	# Gnu parallel has to be installed
	parallel "rm {}" ::: ${dirSample}/*_polygon/TCGA-*.svs/*-features.csv
    fi
fi

# After the first part has finished run this
if [ $step == 2 ]; then
    for s in `ls -d ./data/features/${cancer_type}/TCGA-*` # for each sample
    do
	sample_id=`echo "${s}" | cut -d '/' -f4`           # get the sample id
	# If covds data is not already present run the script
	# that generates the covariance descriptor from masks' morphological features
	# the output is stored in the data/covds directory
	[ -f data/covds/${cancer_type}/${sample_id}/*.pkl ] || /usr/local/share/anaconda3/bin/ipython ./py/test.mask2descriptor.py 10 50 ${s}
    done
fi




