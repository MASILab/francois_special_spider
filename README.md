
# francois_special
Francois' Special Spider from XNAT

This pipeline is in fact the fusion of 4 pipelines. Tractoflow, RBx-Flow, Tractometry-Flow and Connectoflow. See below for each pipeline specific description and output.

### Inputs
- dwmri.nii.gz (from dtiQA – PREPROCESSED)
- dwmri.bval (from dtiQA – PREPROCESSED)
- dwmri.bvec (from dtiQA – PREPROCESSED)
- t1.nii.gz (for Slant)
- labels.nii.gz (from Slant)

### Parameters
- sh_order: 8
- dti_shells: "0 1000"
- fodf_shells: "0 1000"
- pft_seed: 10
- pft_mask_type: wm
- local_seed: 10
- local_mask_type: wm
- algo: prob
- nb_run: 27
- vote_ratio: 0.5

### Input assumptions and parameters choice

 1. The diffusion has been preprocessed using the dtiQA_v7 pipeline.
 2. The parameters *dti_shells* and *fodf_shells* must be chosen according to each project's sequence. It can be single-shell or multi-shell. 
 3. The acquisition is adequate for tensor reconstruction, 800 < BVAL < 1200, with at least 12 directions.
 4. The acquistion is adequate for fODF reconstruction, 800 < BVAL < 3000, with at least 32 directions.
 5. The parameters *sh_order* (default: 8) is the order of spherical harmonics used for fODF. If your fodf_shells has less than 45 directions, used 6.
 6. *pft_mask_type* and *local_mask_type* (default: wm) defines the initialization "tissue" for tractography. If there is a chance for lesions and tissue segmentation is likely to fail, we recommand switching to fa.
 7. *pft_seed* and *local_seed* (default: 10) define the number of streamlines to initialize per voxel of white matter (or fa).
 8. If tracking is not desired or will be performed outside of the spider, use the smallest values possible (1). 
 9. The *algo* parameter is the choice of tractography algorithm (probabilistic). It is recommanded for most situation, if you want deterministic tractography switch to det.

# tractoflow_spider
Tractoflow Spider from XNAT

TractoFlow [1] pipeline is developed by the Sherbrooke Connectivity Imaging Lab (SCIL) in order to process diffusion MRI dataset from the raw data to the tractography. The pipeline is based on Nextflow [2].
This pipeline is optimized for healthy human adults.

TractoFlow pipeline consist of 23 different steps : 14 steps for the diffusion weighted image (DWI) processing and 8
steps for the T1 weighted image processing.
See https://tractoflow-documentation.readthedocs.io/en/latest/index.html and [1] for more details.

    [1] Theaud, G., Houde, J.-C., Boré, A., Rheault, F., Morency, F., Descoteaux, M.,
        "TractoFlow: A robust, efficient and reproducible diffusion MRI pipeline leveraging Nextflow & Singularity",
        NeuroImage (2020).

    [2] Paolo Di Tommaso, et al. "Nextflow enables reproducible computational workflows.", Nature Biotechnology 35, 316-319
        (2017)

    [3] Garyfallidis, E., Brett, M., Amirbekian, B., Rokem, A., Van Der Walt, S., Descoteaux, M., Nimmo-Smith, I.,
        "Dipy, a library for the analysis of diffusion mri data.", Frontiers in neuroinformatics (2014) 8, 8.

    [4] Tournier, J. D., Smith, R. E., Raffelt, D. A., Tabbara, R., Dhollander, T., Pietsch, M., & Connelly, A.,
        "MRtrix3: A fast, flexible and open software framework for medical image processing and visualisation.",
        Neuroimage (2020).

    [5] Avants, B.B., Tustison, N., Song, G., "Advanced normalization tools (ants)." Insight J (2009) 2, 1-35.

    [6] Jenkinson, M., Beckmann, C.F., Behrens, T.E., Woolrich, M.W., Smith, S.M., "Fsl." Neuroimage 62 (2012), 782-790.

### Outputs
**Reporting**
- readme.txt
- report.html
- report.pdf

**DWI**
- dwi.bval
- dwi.bvec
- dwi_resampled.nii.gz
- b0_mask_resampled.nii.gz
- b0_resampled.nii.gz

**DTI_mtrics**
- fa.nii.gz
- md.nii.gz
- rd.nii.gz
- ad.nii.gz
- rgb.nii.gz
- tensor.nii.gz
- evals_e1.nii.gz
- evecs_v1.nii.gz

**FODF_metrics**
- fodf.nii.gz
- peaks.nii.gz
- nufo.nii.gz
- afd_max.nii.gz
- afd_sum.nii.gz
- afd_total.nii.gz

**Register T1w**
- t1_mask_warped.nii.gz
- t1_warped.nii.gz
- output0GenericAffine.mat
- output1InverseWarp.nii.gz
- output1Warp.nii.gz

**Tissue segmentation**
- mask_csf.nii.gz
- mask_gm.nii.gz
- mask_wm.nii.gz
- map_csf.nii.gz
- map_gm.nii.gz
- map_wm.nii.gz

**Tractography masks**
- map_exclude.nii.gz
- map_include.nii.gz
- interface.nii.gz
- local_seeding_mask.nii.gz
- local_tracking_mask.nii.gz
- pft_seeding_mask.nii.gz

**Tracking**
- local.trk
- pft.trk

# rbx_flow_spider
RBX Flow Spider from XNAT

RecobundlesX is a multi-atlas, multi-parameters version of Recobundles [1, 2]. It is optimized for whole brain coverage using 39 major well-known white matter pathways. The atlas is a customized population average from 20 UKBioBank [3] and 20 Human Connectome Project [4] datasets co-registered to MNI152 space.

This atlas was made to cover as much spatial extend as possible and explore as much shape variability as possible. Recobundles is when run 27 times with bundle-specific paramters and the results of each execution are used in a majority-vote approach. This is inspired from the state-of-the-art in medical images segmentation (before machine-learning) [5,6].

Then, a shape-based pruning is applied to each bundle to remove inconsistent or spurious streamlines (outliers) [7].
See https://zenodo.org/record/4630660# for more details.

### References
    [1] Garyfallidis, Eleftherios, et al. "Recognition of white matter bundles using local and global
        streamline-based registration and clustering." NeuroImage 170 (2018): 283-295.

    [2] Rheault, François. "Analyse et reconstruction de faisceaux de la matière blanche." Computer Science
        (Université de Sherbrooke) (2020), https://savoirs.usherbrooke.ca/handle/11143/17255

    [3] Sudlow, Cathie, et al. "UK biobank: an open access resource for identifying the causes of a wide range of complex
        diseases of middle and old age." Plos med 12.3 (2015): e1001779.

    [4] Van Essen, David C., et al. "The WU-Minn human connectome project: an overview." Neuroimage 80 (2013): 62-79.

    [5] Iglesias, Juan Eugenio, and Mert R. Sabuncu. "Multi-atlas segmentation of biomedical images: a survey."
        Medical image analysis 24.1 (2015): 205-219.

    [6] Pipitone, Jon, et al. "Multi-atlas segmentation of the whole hippocampus and subfields using multiple automatically
        generated templates." Neuroimage 101 (2014): 494-512.

    [7] Côté, Marc-Alexandre, et al. "Cleaning up the mess: tractography outlier removal using hierarchical QuickBundles
        clustering." 23rd ISMRM annual meeting. Toronto, Canada. 2015.

### Outputs
**Reporting**
- report.html
- report.pdf

**Bundles**
- *_cleaned.trk

**Centroids**
- *_centroids.trk

# tractometry_flow_spider
Tractometry Flow Spider from XNAT

This pipeline allows you to extract tractometry information by combining subjects' 
WM bundles and diffusion MRI metrics. There is two way the tractometry informatin is computed:
- Average metric inside of a WM bundle volume (voxels occupied by at least one streamline)
- Average metric inside of a subsection of WM bundle volume (voxels occupied by at least one streamline)

The second method 'cut' the bundle in section so variation can be observed along the length. The exact steps are described in [1]. This approach is similar to what is presented in [1,2].
All reported metrics are weighted by streamline density, this way the values of the core/center of bundles are more represented than spurious streamlines and outliers.

Bundle_Metrics_Stats_In_Endpoints/ contains maps for each bundle where the average value along a streamlines are projected to the last points for cortical projection visualisation or statistics.

To fully QA the data, we recommand to download the labels map TRK file and inspect them in MI-Brain (https://www.imeka.ca/mi-brain/). The pipeline was optimized for bundles with large spatial extend (probabilistic tractography) extracted with RecobundlesX using this atlas: https://zenodo.org/record/4630660#.


### References
    [1] Cousineau, Martin, et al. "A test-retest study on Parkinson's PPMI dataset yields statistically significant white matter fascicles. "NeuroImage: Clinical 16, 222-233 (2017) doi:10.1016/j.nicl.2017.07.020

    [2] Yeatman, Jason D., et al. "Tract profiles of white matter properties: automating fiber-tract quantification." PloS one 7.11 (2012): e49790.

    [3] Chandio, Bramsh Qamar, et al. "Bundle analytics, a computational framework for investigating the shapes and profiles of brain pathways across populations." Scientific reports 10.1 (2020): 1-18.

### Outputs
**Reporting**
- report.html
- report.pdf

**Bundles statistics**
- stats_xlsx/
- stats_json/

**Bundle maps**
- labels_maps/
- bundle_endpoints_metrics/

# connectoflow_spider
Connectoflow Spider from XNAT

Connectoflow [1] is Nextflow [2] pipeline to generate Connectomics [3,4] matrices from tractography data.
The key steps in this version of Connectoflow are:
- Decompose: This step performs the parcel-to-parcel decomposition of the tractogram. It includes streamline-cutting
    operations to ensure streamlines have terminations in the provided atlas. Moreover, connection-wise cleaning processes
    that remove loops, discard spurious streamlines and discard incoherent curvatures are used to remove as many false
    positives as possible [5].
- COMMIT: To further decrease the number of invalid streamlines and assign a quantitative weight to each streamline,
    Convex Optimization Modeling for Micro-structure Informed Tractography (COMMIT) [6,7] is used. This not only allows the
    removal of aberrant or spurious streamlines, but it was shown to increase reproducibility of connectivity measures by
    being more robust to various tractography biases. 
- AFD: Apparent Fiber Density (AFD) [8,9] is subsequently computed connection-wise using streamline orientations
    (fixel), which can be computationally burdensome if done on every pairwise connection of the connectome a posteriori.
    This step will provide a AFD-weighted connectivity matrix.

### References
    [1] Rheault, Francois, et al. "Connectoflow: A cutting-edge Nextflow pipeline for structural connectomics", ISMRM 2021 Proceedings, #710. 
    
    [2] Di Tommaso, Paolo, et al. "Nextflow enables reproducible  computational workflows.", Nature biotechnology 35.4 (2017): 316-319. 
    
    [3] Sotiropoulos, Stamatios N., and Andrew Zalesky. "Building connectomes using diffusion MRI: why, how and but.", NMR in Biomedicine 32.4 (2019): e3752.
    
    [4] Yeh, Chun-Hung, et al. "Mapping structural connectivity using diffusion MRI: challenges and opportunities.", Journal of Magnetic Resonance Imaging (2020). 
    
    [5] Zhang, Zhengwu, et al. "Mapping population-based structural connectomes.", NeuroImage 172 (2018): 130-145. 
    
    [6] Daducci, Alessandro, et al. "COMMIT: convex optimization modeling for microstructure informed tractography.", IEEE transactions on medical imaging 34.1 (2014): 246-257. 
    
    [7] Schiavi, Simona, et al. "A new method for accurate in vivo mapping of human brain connections using microstructural, and anatomical information." Science advances 6.31 (2020): eaba8245. 
    
    [8] Raffelt, David A., et al. "Investigating white matter fibre density and morphology using fixel-based analysis.", Neuroimage 144 (2017): 58-73. 
    
    [9] Dhollander, Thijs, et al. "Fixel-based Analysis of Diffusion MRI: Methods, Applications, Challenges and Opportunities." (2020).

### Outputs
**Reporting**
- report.html
- report.pdf

**Connectivity matrices**
- *.npy

**MNI space data**
- mni_icbm152_nlin_asym_09c_t1_masked.nii.gz (template)
- labels_warped_mni_int16.nii.gz
- t1_mni.nii.gz
- decompose_warped_mni.h5

**Transforms to MNI**
- to_mni0GenericAffine.mat
- to_mni1Warp.nii.gz
- to_mni1InverseWarp.nii.gz
