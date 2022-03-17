#!/bin/bash

IN_DIR=${1}
OUT_DIR=${2}
N_SUBJ=${3}
N_SESS=${4}
BUNDLES_DIR=${5}
CENTROIDS_DIR=${6}
NB_PTS=${7}

# Prepare input for Tractometry Flow
mkdir raw_2/${N_SUBJ}_${N_SESS}/metrics/ -p
cp ${IN_DIR}/${BUNDLES_DIR} raw_2/${N_SUBJ}_${N_SESS}/bundles -r
cp ${IN_DIR}/${CENTROIDS_DIR} raw_2/${N_SUBJ}_${N_SESS}/centroids -r
for i in ${IN_DIR}/metrics_*.nii.gz; do base_name=$(basename $i); cp ${i} raw_2/${N_SUBJ}_${N_SESS}/metrics/${base_name/metrics_/}; done

# Launch pipeline
/nextflow /tractometry_flow/main.nf --input raw_2/ --nb_points ${NB_PTS} --skip_projection_endpoints_metrics false \
	--bundle_suffix_to_remove _cleaned --colors '{"AC":"0x02d983","AF_L":"0xcc0000","AF_R":"0xffdf0f","CC_Fr_1":"0x0d6cbf","CC_Fr_2":"0xbf0099","CC_Oc":"0xf20505","CC_Pa":"0x9ad909","CC_Pr_Po":"0x04bf74","CC_Te":"0x0418cc","CG_L":"0xe605b9","CG_R":"0xff6f00","FAT_L":"0x89bf0b","FAT_R":"0x14ffa1","FPT_L":"0x0f27ff","FPT_R":"0xd90452","FX_L":"0xbf5504","FX_R":"0xb8ff12","ICP_L":"0x08c5cc","ICP_R":"0x5a0ff2","IFOF_L":"0xff0862","IFOF_R":"0xe56a0b","ILF_L":"0x3ccc08","ILF_R":"0x13ebf2","MCP":"0x4e0ecc","MdLF_L":"0xbf0c4d","MdLF_R":"0xd9bd09","OR_ML_L":"0x02f22a","OR_ML_R":"0x0074d9","PC":"0xa809d9","POPT_L":"0xbfa708","POPT_R":"0x08bf26","PYT_L":"0x0d8eff","PYT_R":"0xc60dff","SCP_L":"0x02d983","SCP_R":"0x0d6cbf","SLF_L":"0xbf0099","SLF_R":"0xf20505","UF_L":"0x9ad909","UF_R":"0x04bf74"}' \
	--processes 1 -resume -with-report report.html

# Generate labels map screenshot for major bundles Q/A
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/screenshot_bundle_coloring.py results_tractometry/*/*/*__AF_L_labels.trk ${IN_DIR}/metrics_fa.nii.gz \
	--reference_coloring results_tractometry/*/*/*__AF_L_labels.nii.gz --anat_opacity 0.0 \
	--target_template /mni_icbm152_nlin_asym_09c_t1_masked_2mm.nii.gz --out_dir AF_L
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/screenshot_bundle_coloring.py results_tractometry/*/*/*__AF_R_labels.trk ${IN_DIR}/metrics_fa.nii.gz \
	--reference_coloring results_tractometry/*/*/*__AF_R_labels.nii.gz --anat_opacity 0.0 --right \
	--target_template /mni_icbm152_nlin_asym_09c_t1_masked_2mm.nii.gz --out_dir AF_R
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/screenshot_bundle_coloring.py results_tractometry/*/*/*__CC_Fr_2_labels.trk ${IN_DIR}/metrics_fa.nii.gz \
	--reference_coloring results_tractometry/*/*/*__CC_Fr_2_labels.nii.gz --anat_opacity 0.0 \
	--target_template /mni_icbm152_nlin_asym_09c_t1_masked_2mm.nii.gz --out_dir CC_Fr_2
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/screenshot_bundle_coloring.py results_tractometry/*/*/*__CC_Pr_Po_labels.trk ${IN_DIR}/metrics_fa.nii.gz \
	--reference_coloring results_tractometry/*/*/*__CC_Pr_Po_labels.nii.gz --anat_opacity 0.0 \
	--target_template /mni_icbm152_nlin_asym_09c_t1_masked_2mm.nii.gz --out_dir CC_Pr_Po
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/screenshot_bundle_coloring.py results_tractometry/*/*/*__PYT_L_labels.trk ${IN_DIR}/metrics_fa.nii.gz \
	--reference_coloring results_tractometry/*/*/*__PYT_L_labels.nii.gz --anat_opacity 0.0 \
	--target_template /mni_icbm152_nlin_asym_09c_t1_masked_2mm.nii.gz --out_dir PYT_L
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	python3.8 /CODE/screenshot_bundle_coloring.py results_tractometry/*/*/*__PYT_R_labels.trk ${IN_DIR}/metrics_fa.nii.gz \
	--reference_coloring results_tractometry/*/*/*__PYT_R_labels.nii.gz --anat_opacity 0.0 --right \
	--target_template /mni_icbm152_nlin_asym_09c_t1_masked_2mm.nii.gz --out_dir PYT_R

# Generate profile plot for Q/A
echo '{"AC":"0x02d983","AF_L":"0xcc0000","AF_R":"0xffdf0f","CC_Fr_1":"0x0d6cbf","CC_Fr_2":"0xbf0099","CC_Oc":"0xf20505","CC_Pa":"0x9ad909","CC_Pr_Po":"0x04bf74","CC_Te":"0x0418cc","CG_L":"0xe605b9","CG_R":"0xff6f00","FAT_L":"0x89bf0b","FAT_R":"0x14ffa1","FPT_L":"0x0f27ff","FPT_R":"0xd90452","FX_L":"0xbf5504","FX_R":"0xb8ff12","ICP_L":"0x08c5cc","ICP_R":"0x5a0ff2","IFOF_L":"0xff0862","IFOF_R":"0xe56a0b","ILF_L":"0x3ccc08","ILF_R":"0x13ebf2","MCP":"0x4e0ecc","MdLF_L":"0xbf0c4d","MdLF_R":"0xd9bd09","OR_ML_L":"0x02f22a","OR_ML_R":"0x0074d9","PC":"0xa809d9","POPT_L":"0xbfa708","POPT_R":"0x08bf26","PYT_L":"0x0d8eff","PYT_R":"0xc60dff","SCP_L":"0x02d983","SCP_R":"0x0d6cbf","SLF_L":"0xbf0099","SLF_R":"0xf20505","UF_L":"0x9ad909","UF_R":"0x04bf74"}' >> tmp_dict.json
xvfb-run -a --server-num=$((65536+$$)) --server-args="-screen 0 1600x1280x24 -ac" \
	scil_plot_mean_std_per_point.py results_tractometry/*/Bundle_Mean_Std_Per_Point/*__mean_std_per_point.json tmp_dict/ --dict_colors tmp_dict.json

# Generate PDF
python3.8 /CODE/generate_tractometry_flow_spider_pdf.py ${N_SUBJ}_${N_SESS} ${NB_PTS}

# Copy relevant outputs
cp report.pdf ${OUT_DIR}/report_tmf.pdf
cp report.html ${OUT_DIR}/report_tmf.html
mkdir ${OUT_DIR}/stats_xlsx/; cp results_tractometry/Statistics/*.xlsx ${OUT_DIR}/stats_xlsx/
mkdir ${OUT_DIR}/stats_json/; cp results_tractometry/Statistics/*.json ${OUT_DIR}/stats_json/
mkdir ${OUT_DIR}/labels_maps/; cp results_tractometry/*/*/*__*_labels.nii.gz results_tractometry/*/*/*__*_labels.trk ${OUT_DIR}/labels_maps/
mkdir ${OUT_DIR}/bundle_endpoints_metrics/
for i in results_tractometry/*/Bundle_Endpoints_Metrics/*; do base_name=$(basename ${i}); for j in ${i}/*; do base_name_2=$(basename ${j}); cp ${j} ${OUT_DIR}/bundle_endpoints_metrics/${base_name_2/${N_SUBJ}_${N_SESS}__/${N_SUBJ}_${N_SESS}__${base_name}_}; done; done

rm *html* *pdf*