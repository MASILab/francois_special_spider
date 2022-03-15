#!/bin/bash

IN_DIR=${1}
OUT_DIR=${2}
N_SUBJ=${3}
N_SESS=${4}
IN_DWI=${5}
IN_BVAL=${6}
IN_BVEC=${7}
IN_PEAKS=${8}
IN_FODF=${9}
IN_AFF=${10}
IN_WARP=${11}
IN_ENSEMBLE=${12}
IN_T1=${13}
IN_LABELS=${14}
IN_LESIONS=${15}
IN_LABELS_TO_REMOVE=${16}

# Prepare input for Connectoflow
cd /TMP/
mkdir raw/${N_SUBJ}_${N_SESS}/metrics/ -p
cp ${IN_DIR}/${IN_DWI} raw/${N_SUBJ}_${N_SESS}/dwi.nii.gz
cp ${IN_DIR}/${IN_BVAL} raw/${N_SUBJ}_${N_SESS}/dwi.bval
cp ${IN_DIR}/${IN_BVEC} raw/${N_SUBJ}_${N_SESS}/dwi.bvec
cp ${IN_DIR}/${IN_PEAKS} raw/${N_SUBJ}_${N_SESS}/peaks.nii.gz
cp ${IN_DIR}/${IN_FODF} raw/${N_SUBJ}_${N_SESS}/fodf.nii.gz
cp ${IN_DIR}/${IN_AFF} raw/${N_SUBJ}_${N_SESS}/output0GenericAffine.mat
cp ${IN_DIR}/${IN_WARP} raw/${N_SUBJ}_${N_SESS}/output1Warp.nii.gz
cp ${IN_DIR}/${IN_ENSEMBLE} raw/${N_SUBJ}_${N_SESS}/tracking.trk
cp ${IN_DIR}/${IN_LESIONS} raw/${N_SUBJ}_${N_SESS}/lesion_mask.nii.gz
for i in ${IN_DIR}/metrics_*.nii.gz; do base_name=$(basename $i); cp ${i} raw/${N_SUBJ}_${N_SESS}/metrics/${base_name/metrics_/}; done

# Data from Slant must be slightly modified for Connectoflow
scil_image_math.py lower_threshold ${IN_DIR}/${IN_LABELS} 0.01 brain_mask.nii.gz --data_type uint8
scil_image_math.py multiplication brain_mask.nii.gz ${IN_DIR}/${IN_T1} raw/${N_SUBJ}_${N_SESS}/t1.nii.gz --data_type float32
scil_image_math.py convert ${IN_DIR}/${IN_LABELS} raw/${N_SUBJ}_${N_SESS}/labels.nii.gz --data_type uint16
scil_remove_labels.py raw/${N_SUBJ}_${N_SESS}/labels.nii.gz raw/${N_SUBJ}_${N_SESS}/labels.nii.gz -f -i ${IN_LABELS_TO_REMOVE}
scil_dilate_labels.py raw/${N_SUBJ}_${N_SESS}/labels.nii.gz raw/${N_SUBJ}_${N_SESS}/labels.nii.gz -f --mask brain_mask.nii.gz
python3.8 /CODE/get_labels_list.py raw/${N_SUBJ}_${N_SESS}/labels.nii.gz labels_list.txt

# Launch pipeline
/nextflow /connectoflow/main.nf --input raw/ --template /mni_icbm152_nlin_asym_09c_t1_masked.nii.gz \
	--labels_list labels_list.txt --use_similarity_metric false --use_commit2 --ball_stick --iso_diff "2.0E-3" \
	--processes_register 1 --processes_commit 1 --processes_afd_rd 1 --processes_connectivity 1 --processes 1 \
	-resume -with-report report.html

# Generate PDF
python3.8 /CODE/generate_connectoflow_spider_pdf.py ${N_SUBJ}_${N_SESS} 

# Copy relevant outputs
cp report.pdf report.html ${OUT_DIR}/
cp /mni_icbm152_nlin_asym_09c_t1_masked.nii.gz ${OUT_DIR}/mni_icbm152_nlin_asym_09c_t1_masked.nii.gz
cp results_conn/*/*/*__decompose_warped_mni.h5 results_conn/*/*/*__labels_warped_mni_int16.nii.gz ${OUT_DIR}/
cp results_conn/*/*/*__outputWarped.nii.gz ${OUT_DIR}/${N_SUBJ}_${N_SESS}__t1_mni.nii.gz
cp results_conn/*/*/*__output0GenericAffine.mat results_conn/*/*/*__output1InverseWarp.nii.gz results_conn/*/*/*__output1Warp.nii.gz ${OUT_DIR}/
mkdir ${OUT_DIR}/connectivity_matrices/
for i in results_conn/*/Compute_Connectivity/*.npy; do cp ${i} ${OUT_DIR}/connectivity_matrices/${N_SUBJ}_${N_SESS}__$(basename ${i}); done