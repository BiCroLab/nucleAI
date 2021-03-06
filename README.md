nucleAI
==============================

machine learning on WSI

Project Organization
------------
```bash
.
├── data
│   ├── covds		<- temporary dir storing covariance descriptors per sample
│   └── features	<- temportary dir storing morphological features per sample
├── docs		<- Documentation about the project
├── models		<- Trained and serialized models, model predictions, or model summaries
├── notebooks		<- jupyter notebooks used in this project
└── py			<- python scripts used in this project
```
The requirements.txt file list the working environment used when the pipeline was run, though not all packages listed in the file might be necessary. 

List of main scripts:
```bash
./scripts.sh		<- used to generate features and descriptors for a given cancer type
./script.intensity.sh	<- called by scripts.sh used either to generate features or descriptors
./covd2umap.sh		<- used to get the umap projection of a collection of descriptors
./py/test.covd_with_intensity_parallelOverPatches.py	   <- called by script.intensity.sh, used to get the morphological features
./py/test.mask2descriptor.py				   <- called by script.intensity.sh, used to get the descriptors
./py/test.covd_2dProjection.py				   <- called by covd2umap.sh, used to get the umap projection for a collection of descriptors
```
To run the pipeline, make sure that the raw svs files and the polygon data are located in a directory with the same structure as the original one:
```bash
/media/garner1/hdd2/svs_BRCA   <- example dirpath to BRCA svs samples, with subdirectory per each sample
/media/garner1/hdd2/TCGA_polygons/BRCA/TCGA-05-4245-01Z-00-DX1...svs.tar.gz <- example dirpath to single BRCA sample polygon file
```
Also, make sure that the anaconda folder is located as expected in the script.intensity.sh (open the script and check where it has been hard-coded)

Then open the scripts.sh file and edit the type of cancer that you want to process (BRCA, LUAD, etc.). Save and exit.

Then run 
```bash
bash scripts.sh
```

The data folder will contain the output for both morphological features and covariance descriptors.

To get the UMAP representation of the descriptors see the content of covd2umap.sh to have examples for different cancer types, or to get the global TCGA projection. 
At the moment of writing these notes a bug seems to affet the umap-learn library when run on numbers of samples exceeding few towsand elements: https://github.com/lmcinnes/umap/issues/496

The UMAP projection still works when run on individual cancer-types.

