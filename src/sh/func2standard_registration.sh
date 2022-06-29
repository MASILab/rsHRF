#!/bin/bash

folder='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/ADNI_23/'
atlas='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii'

i=0
cd $folder
for subject in * ; do
 if [ -d "$subject" ]; then
  subject_dir="${folder}${subject}/"
  cd $subject_dir
   for exp in * ]; do
    if [ -d  "${exp}/func2standard" ] ; then
     if [[ "$i" -ge 0 ]]; then
      exp_dir="${subject_dir}${exp}/"

      cd $exp_dir
      param='hrf'
      
      # input files
      func='rsfmri/Deconv_Detrend_4DVolume_'$param'.nii'
      func_dir='rsfmri'
      T1="anat/T1_copy.nii.gz"

      # directories
      dir_func2struct_param="func2struct/"
      dir_func2stand="func2stand/"
      # mkdir "func2struct/"$param
      # new files
      T1_brain="anat/brain_masked.nii.gz"
      func2struct_param=$dir_func2struct_param"/"$param"/"$param
      
      # command=`python3 /home/local/VANDERBILT/dolel/Documents/rsHRF/src/py/brain_extraction.py \
      #   --T1 ${T1} --out_mask ${T1_brain}`
 

      echo $i  "-----${subject_dir}${exp}------ $param"

      # epi_reg --epi=$func --t1=$T1 --t1brain=$T1_brain --out=$func2struct_param
      # convertwarp -r ${dir_func2struct_param}mean_func2struct.nii.gz   -m ${dir_func2struct_param}"mean_func2struct.mat" -o ${dir_func2struct_param}"mean_func2struct_warp.nii.gz"
      
      applywarp -i $func  -r ${dir_func2struct_param}"Height/func2structHeight.nii.gz"  -w ${dir_func2struct_param}"Height/func2struct_warp.nii.gz" --interp=spline -o  "func2struct/"$param"/func2struct_"$param.nii.gz
      
      # echo=`python3 /home/local/VANDERBILT/dolel/Documents/rsHRF/src/py/registration_func2_stand_ants.py \
      #   --T1 ${T1} --rsfmri ${dir_func2struct_param} --atlas ${atlas} --func2stand ${dir_func2stand}`
      
      cd ..
     fi
     i=$((i+1))
    fi
   done
  cd ..
  fi
done

