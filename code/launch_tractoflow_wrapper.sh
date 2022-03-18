#!/bin/bash

IN_DIR=${1}
OUT_DIR=${2}
N_SUBJ=${3}
N_SESS=${4}
IN_T1=${5}
IN_DWI=${6}
IN_BVAL=${7}
IN_BVEC=${8}

# Prepare input for Tractoflow
mkdir raw_0/${N_SUBJ}_${N_SESS} -p
cp ${IN_DIR}/${IN_T1} raw_0/${N_SUBJ}_${N_SESS}/t1.nii.gz
cp ${IN_DIR}/${IN_DWI} raw_0/${N_SUBJ}_${N_SESS}/dwi.nii.gz
cp ${IN_DIR}/${IN_BVAL} raw_0/${N_SUBJ}_${N_SESS}/bval
cp ${IN_DIR}/${IN_BVEC} raw_0/${N_SUBJ}_${N_SESS}/bvec

# Relevant parameters for Tractoflow
SH_ORDER=${9}
DTI_SHELLS=${10}
FODF_SHELLS=${11}
PFT_SEED=${12}
PFT_MASK_TYPE=${13}
LOCAL_SEED=${14}
LOCAL_MASK_TYPE=${15}
ALGO=${16}

# Launch pipeline
/nextflow /tractoflow/main.nf \
	--input raw_0/ --dti_shells "${DTI_SHELLS}" --fodf_shells "${FODF_SHELLS}" --run_dwi_denoising false --run_topup false \
	--run_eddy false --use_slice_drop_correction false --mean_frf false --sh_order ${SH_ORDER} --run_pft_tracking true \
	--pft_algo ${ALGO} --pft_seeding_mask_type ${PFT_MASK_TYPE} --pft_nbr_seeds ${PFT_SEED} --run_local_tracking true \
	--local_algo ${ALGO} --local_tracking_mask_type ${LOCAL_MASK_TYPE} --local_nbr_seeds ${LOCAL_SEED} --processes_denoise_dwi 1 \
	--processes_denoise_t1 1 --processes_eddy 1 --processes_fodf 1 --processes 1 --processes_brain_extraction_t1 1 \
	--processes_registration 1 -resume -with-report report.html

# scil_remove_invalid_streamlines.py facilitate usage if data is downloaded and used with other tools (Dipy/Scilpy)
# Screenshot the tracking for QA
scil_remove_invalid_streamlines.py results/*/PFT_Tracking/*.trk ${N_SUBJ}_${N_SESS}__pft.trk --cut_invalid --remove_single_point --remove_overlapping_points
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	scil_visualize_bundles_mosaic.py results/*/DTI_Metrics/*__fa.nii.gz \
	${N_SUBJ}_${N_SESS}__pft.trk pft.png --resolution_of_thumbnails 600 --opacity_background 0.5 --zoom 1.5

scil_remove_invalid_streamlines.py results/*/Local_Tracking/*.trk ${N_SUBJ}_${N_SESS}__local.trk --cut_invalid --remove_single_point --remove_overlapping_points
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	scil_visualize_bundles_mosaic.py results/*/DTI_Metrics/*__fa.nii.gz \
	${N_SUBJ}_${N_SESS}__local.trk local.png --resolution_of_thumbnails 600 --opacity_background 0.5 --zoom 1.5

convert pft.png -crop 600x3600+600+0 pft.png
convert local.png -crop 600x3600+600+0 local.png

# Screenshot FODF in two views for QA
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	scil_visualize_fodf.py results/*/FODF_Metrics/*__fodf.nii.gz --axis_name axial --output axial.png --silent \
	--background results/*/DTI_Metrics/*__fa.nii.gz --win_dims 2560 2560
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	scil_visualize_fodf.py results/*/FODF_Metrics/*__fodf.nii.gz --axis_name coronal --output coronal.png --silent \
	--background results/*/DTI_Metrics/*__fa.nii.gz --win_dims 2560 2560

# Generate PDF
python3.8 /CODE/generate_tractoflow_spider_pdf.py ${N_SUBJ}_${N_SESS} 

# Copy relevant outputs
cp results/*/readme.txt ${OUT_DIR}/
cp report.pdf ${OUT_DIR}/report_tf.pdf
cp report.html ${OUT_DIR}/report_tf.html
cp -L results/*/*/*__b0_resampled.nii.gz results/*/*/*__b0_mask_resampled.nii.gz results/*/*/*__dwi_resampled.nii.gz ${OUT_DIR}/
cp -L raw_0/${N_SUBJ}_${N_SESS}/bval ${OUT_DIR}/${N_SUBJ}_${N_SESS}__dwi.bval
cp -L raw_0/${N_SUBJ}_${N_SESS}/bvec ${OUT_DIR}/${N_SUBJ}_${N_SESS}__dwi.bvec
cp -L results/*/*/*__output0GenericAffine.mat results/*/*/*__output1InverseWarp.nii.gz results/*/*/*__output1Warp.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__t1_mask_warped.nii.gz results/*/*/*__t1_warped.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__map_csf.nii.gz results/*/*/*__map_gm.nii.gz results/*/*/*__map_wm.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__mask_csf.nii.gz results/*/*/*__mask_gm.nii.gz results/*/*/*__mask_wm.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__local_seeding_mask.nii.gz results/*/*/*__local_tracking_mask.nii.gz results/*/*/*__pft_seeding_mask.nii.gz  ${OUT_DIR}/
cp -L results/*/*/*__map_exclude.nii.gz results/*/*/*__map_include.nii.gz results/*/*/*__interface.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__ad.nii.gz results/*/*/*__rd.nii.gz results/*/*/*__fa.nii.gz results/*/*/*__rgb.nii.gz results/*/*/*__md.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__tensor.nii.gz results/*/*/*__evecs_v1.nii.gz results/*/*/*__evals_e1.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__afd_max.nii.gz results/*/*/*__afd_sum.nii.gz results/*/*/*__afd_total.nii.gz results/*/*/*__nufo.nii.gz ${OUT_DIR}/
cp -L results/*/*/*__peaks.nii.gz results/*/*/*__fodf.nii.gz ${OUT_DIR}/
scil_streamlines_math.py concatenate ${N_SUBJ}_${N_SESS}__pft.trk ${N_SUBJ}_${N_SESS}__local.trk ${OUT_DIR}/${N_SUBJ}_${N_SESS}__ensemble.trk

rm *html* *png* *trk* *pdf*
