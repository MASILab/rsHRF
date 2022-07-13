#!/bin/bash

folder='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/ADNI_23/'
atlas='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii'

params="Olrm_Height DipHeight TroughHeight PeakIntegral DipIntegral TroughIntegral Olrm_Time2peak Time2dip Time2trough Olrm_FWHM"

i=0
cd $folder
for subject in * ; do
 if [ -d "$subject" ]; then
  subject_dir="${folder}${subject}/"
  cd $subject_dir
   for exp in * ]; do
    if [ -d  "${exp}/func2standard" ] ; then
     if [[ "$i" -ge 700 ]]; then
      exp_dir="${subject_dir}${exp}/"

      cd $exp_dir      
      # input files
      func_dir='rsfmri'
      T1="anat/T1_copy.nii.gz"

      # directories
      dir_func2struct="func2struct_canonical/"
      dir_func2stand="func2stand_canonical/"
 
      # echo $pwd
      #### on mean brain
      # epi_reg --epi=$func --t1=$T1 --t1brain=$T1_brain --out=$func2struct_param
      
      echo $i  "-----${subject_dir}${exp}------"
      if [[ ! -f $dir_func2stand"func2stand_DipHeight.nii.gz" ]]
      then
      #   convertwarp -r func2struct/mean_func2struct.nii.gz   -m func2struct"/mean_func2struct.mat" -o func2struct"/mean_func2struct_warp.nii.gz"
      # fi
      
      # for val in $params; do
      #     func='rsfmri/Deconv_Canonical_Detrend_4DVolume_'$val'.nii'
      #     applywarp -i $func  -r func2struct"/mean_func2struct.nii.gz"  -w func2struct"/mean_func2struct_warp.nii.gz" --interp=spline -o  $dir_func2struct"func2struct_"$val.nii.gz
      # done
        python3 /home/local/VANDERBILT/dolel/Documents/rsHRF/src/py/registration_func2_stand_ants.py --T1 ${T1} --rsfmri ${dir_func2struct} --atlas ${atlas} --func2stand ${dir_func2stand}

      fi

      
      cd ..
     fi
     i=$((i+1))
    fi
   done
  cd ..
  fi
done
