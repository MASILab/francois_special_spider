

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


### Inputs
- bundles/*.trk (from RBX Flow)
- centroids/*.trk (from RBX Flow)
- fa.nii.gz (from Tractoflow)
- md.nii.gz (from Tractoflow)
- rd.nii.gz (from Tractoflow)
- ad.nii.gz (from Tractoflow)
- nufo.nii.gz (from Tractoflow)
- afd_total.nii.gz (from Tractoflow)
- afd_sum.nii.gz (from Tractoflow)
- afd_max.nii.gz (from Tractoflow)

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

### Input assumptions and parameters choice
Tractogram reconstruction was adequate (millions of streamlines, no lesions unless corrected accordingly)
Bundle segmentation was adaquate (each bundle is dense, without obvious 'defect')
The parameters 'nb_pts' is between 2-100
This pipeline does not perform any statistical analysis, this should be planned separately beforehand
