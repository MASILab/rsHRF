# Characterization of Hemodynamic Response Function (HRF) at resting state
The project uses the SPM12[1] toolbox and the Matlab script from the rsHRF GitHub repository: https://github.com/compneuro-da/rsHRF


* `compute_hrf.m` computes the hrf for every subject of the dataset and the volume of some parameters (Time2Peak, Height…)
* `compute_params_hrf.m`  computes the Time2Dip, DipHeight, DipIntegral and PeakIntegral

The python scripts download the dataset used and list the values of TR used during the MRI acquisition.

## Demo
* `compute_hrf_job(input_dir)` where `input_dir` is the dataset to use. 

* Then, run `compute_params_hrf(input_dir)` to compute the parameters of the HRF.

* To construct the mean population for each parameters of the HRF run `average_population(input_dir, output_dir)`

* It is possible to visualize each nifti files with software like FSL, Slicer...

## References: 
Guo-Rong Wu, Nigel Colenbier, Sofie Van Den Bossche, Kenzo Clauw, Amogh Johri, Madhur Tandon, Daniele Marinazzo. “rsHRF: A Toolbox for Resting-State HRF Estimation and Deconvolution.” Neuroimage, 2021, 244: 118591. DOI:10.1016/j.neuroimage.2021.118591

[1] https://www.fil.ion.ucl.ac.uk/spm/ext/#rsHRF 