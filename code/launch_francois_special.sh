#!/bin/bash

cd "${22}"

# TRACTOFLOW
mkdir output_tf/
bash /CODE/launch_tractoflow_wrapper.sh "${1}" $(readlink -e output_tf/) "${3}" "${4}" "${5}" "${6}" \
	 "${7}" "${8}" "${9}" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}" "${16}"

# RBX_FLOW
mkdir input_rbxf/ output_rbxf/
cp output_tf/*__fa.nii.gz input_rbxf/fa.nii.gz
cp output_tf/*__ensemble.trk input_rbxf/tracking.trk

bash /CODE/launch_rbx_flow_wrapper.sh input_rbxf/ output_rbxf/ "${3}" "${4}" fa.nii.gz \
	tracking.trk "${17}" "${18}"

# TRACTOMETRY_FLOW
mkdir input_tmf/ output_tmf/
cp output_tf/*__ad.nii.gz input_tmf/metrics_ad.nii.gz
cp output_tf/*__rd.nii.gz input_tmf/metrics_rd.nii.gz
cp output_tf/*__fa.nii.gz input_tmf/metrics_fa.nii.gz
cp output_tf/*__md.nii.gz input_tmf/metrics_md.nii.gz
cp output_tf/*__afd_max.nii.gz input_tmf/metrics_afd_max.nii.gz
cp output_tf/*__afd_sum.nii.gz input_tmf/metrics_afd_sum.nii.gz
cp output_tf/*__afd_total.nii.gz input_tmf/metrics_afd_total.nii.gz
cp output_tf/*__nufo.nii.gz input_tmf/metrics_nufo.nii.gz
cp output_rbxf/bundles output_rbxf/centroids input_tmf/ -r

bash /CODE/launch_tractometry_flow_wrapper.sh input_tmf/ output_tmf/ "${3}" "${4}" \
	bundles centroids "${19}"

# CONNECTOFLOW
mkdir input_cf/ output_cf/
cp output_tf/*__ad.nii.gz input_cf/metrics_ad.nii.gz
cp output_tf/*__rd.nii.gz input_cf/metrics_rd.nii.gz
cp output_tf/*__fa.nii.gz input_cf/metrics_fa.nii.gz
cp output_tf/*__md.nii.gz input_cf/metrics_md.nii.gz
cp output_tf/*__afd_max.nii.gz input_cf/metrics_afd_max.nii.gz
cp output_tf/*__afd_sum.nii.gz input_cf/metrics_afd_sum.nii.gz
cp output_tf/*__afd_total.nii.gz input_cf/metrics_afd_total.nii.gz
cp output_tf/*__nufo.nii.gz input_cf/metrics_nufo.nii.gz
cp output_tf/*__dwi_resampled.nii.gz input_cf/dwi_resampled.nii.gz
cp output_tf/*__dwi.bval input_cf/dwi.bval
cp output_tf/*__dwi.bvec input_cf/dwi.bvec
cp output_tf/*__peaks.nii.gz input_cf/peaks.nii.gz
cp output_tf/*__fodf.nii.gz input_cf/fodf.nii.gz
cp output_tf/*__output0GenericAffine.mat input_cf/output0GenericAffine.mat
cp output_tf/*__output1Warp.nii.gz input_cf/output1Warp.nii.gz
cp output_tf/*__ensemble.trk input_cf/tracking.trk
cp "${1}"/"${5}" input_cf/t1.nii.gz
cp "${1}"/"${20}" input_cf/labels.nii.gz
IN_LABELS_TO_REMOVE="${21}"

bash /CODE/launch_connectoflow_wrapper.sh input_cf/ output_cf/ "${3}" "${4}" \
	dwi_resampled.nii.gz dwi.bval dwi.bvec peaks.nii.gz fodf.nii.gz \
	output0GenericAffine.mat output1Warp.nii.gz tracking.trk \
	t1.nii.gz labels.nii.gz "${19}"

cp output*/* "${2}"/ -rL
pdfunite output_tf/*.pdf output_rbxf/*.pdf output_tmf/*.pdf output_cf/*.pdf "${2}"/report.pdf
