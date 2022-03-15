#!/bin/bash

IN_DIR=${1}
OUT_DIR=${2}
N_SUBJ=${3}
N_SESS=${4}
IN_FA=${5}
IN_TRACKING_ENSEMBLE=${6}

# Prepare input for RBX Flow
mkdir raw_1/${N_SUBJ}_${N_SESS} -p
cp ${IN_DIR}/${IN_FA} raw_1/${N_SUBJ}_${N_SESS}/fa.nii.gz
scil_filter_streamlines_by_length.py ${IN_DIR}/${IN_TRACKING_ENSEMBLE} raw_1/${N_SUBJ}_${N_SESS}/tracking.trk --minL 40

# Relevant parameters for RBX Flow
NB_RUN=${7}
VOTE_RATIO=${8}

# Launch pipeline
/nextflow /rbx_flow/main.nf  \
	--input raw_1/ --atlas_config /rbx_pop_average/config.json --atlas_anat /rbx_pop_average/mni_masked.nii.gz \
	--atlas_directory /rbx_pop_average/atlas/ --atlas_centroids /rbx_pop_average/centroids/ \
	--multi_parameters ${NB_RUN} --minimal_vote_ratio ${VOTE_RATIO} --wb_clustering_thr "8 10 12" \
	--register_processes 1 --rbx_processes 1 --processes 1 -resume -with-report report.html

# Screenshot groups of bundles for QA (Hemisphere Left, Right and then commisural pathways)
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/visualize_bundles_mosaic.py raw_1/${N_SUBJ}_${N_SESS}/fa.nii.gz \
	results_rbx/*/Clean_Bundles/*_L_cleaned.trk  left.png --resolution_of_thumbnails 300 --opacity_background 0.5 --zoom 1.5
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/visualize_bundles_mosaic.py raw_1/${N_SUBJ}_${N_SESS}/fa.nii.gz \
	results_rbx/*/Clean_Bundles/*_R_cleaned.trk  right.png --resolution_of_thumbnails 300 --opacity_background 0.5 --zoom 1.5
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/visualize_bundles_mosaic.py raw_1/${N_SUBJ}_${N_SESS}/fa.nii.gz \
	results_rbx/*/Clean_Bundles/*__CC_*_cleaned.trk results_rbx/*/Clean_Bundles/*__MCP_cleaned.trk comm.png \
	--resolution_of_thumbnails 300 --opacity_background 0.5 -f --zoom 1.5

# Generate PDF
python3.8 /CODE/generate_rbx_flow_spider_pdf.py ${N_SUBJ}_${N_SESS} 

# Copy relevant outputss
cp report.pdf ${OUT_DIR}/report_rbxf.pdf
cp report.html ${OUT_DIR}/report_rbxf.html
cp -rL results_rbx/*/Clean_Bundles/ ${OUT_DIR}/bundles
cp -rL results_rbx/*/Transform_Centroids ${OUT_DIR}/centroids

rm *html* *png* *pdf*
