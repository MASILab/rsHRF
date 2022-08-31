#!/bin/bash

Help()
{
# Display Help
echo "Help"
echo "Register data into MNI space"
echo
echo "Syntax: apply_py_parameters.sh [--options]"
echo "options:"
echo "--folder         Input directory containing features csv files "
echo "--atlas          MNI template"
}

while [ "$1" != "" ]; do
    case $1 in
        --folder )  shift
            folder=$1;;
        --atlas )  shift
            atlas=$1;;
        -h | --help )
            Help
            exit;
    esac
    shift
done

i=0
for subject in $folder* ; do
  if [ -d "$subject" ]; then
    for exp in "$subject"/* ; do
      if [ -d "$exp" ]; then
          test=$exp"/Deconv/Deconv_Detrend_4DVolume_DipHeight.nii"
          if [ -f  "$test" ] ; then
            if [ "$i" -ge 1001 ]; then
              echo $i "-----${subject}------"

              func=$subject"/Deconv/Deconv_Detrend_4DVolume_Olrm_Height.nii"

              T1=$subject"/anat/T1.nii.gz"
              T1_brain=$subject"/anat/brain_masked.nii.gz"
              func2struct=$subject"/func2struct/func2struct_Height.nii"

              # directories
              dir_func2struct=$subject"/func2struct/"
              dir_func2stand=$subject"/func2stand/"

              if [[ ! -f $dir_func2stand"func2stand_Time2dip.nii" ]]
              then
                echo "epi_reg_Height"
                mkdir $dir_func2struct
                epi_reg --epi=$func --t1=$T1 --t1brain=$T1_brain --out=$func2struct
              fi

              if [[ ! -f $dir_func2struct"func2struct_Height_warp.nii.gz" ]]
              then
                echo "convertwarp_Height"
                convertwarp -r $dir_func2struct"func2struct_Height.nii.gz"   -m $dir_func2struct"func2struct_Height.mat" -o $dir_func2struct"func2struct_Height_warp.nii.gz"
              fi

              params="Olrm_Time2peak Olrm_FWHM"
              for val in $params; do
                  func=${subject}'/Deconv/Deconv_Detrend_4DVolume_'$val'.nii'
                  if [[ ! -f $dir_func2struct"func2struct_"$val".nii.gz" ]]
                  then
                    echo "func2struct_olrm"
                    applywarp -i $func  -r $dir_func2struct"func2struct_Height.nii.gz"  -w $dir_func2struct"func2struct_Height_warp.nii.gz" --interp=spline -o  $dir_func2struct"func2struct_"$val.nii.gz
                  fi
              done

              params="DipHeight TroughHeight PeakIntegral DipIntegral TroughIntegral Time2dip Time2trough"
              for val in $params; do
                  func=${subject}'/Deconv/'$val'.nii'
                  if [[ ! -f $dir_func2struct"func2struct_"$val".nii.gz" ]]
                  then
                    echo "func2struct_dipHeight"
                    applywarp -i $func  -r $dir_func2struct"func2struct_Height.nii.gz"  -w $dir_func2struct"func2struct_Height_warp.nii.gz" --interp=spline -o  $dir_func2struct"func2struct_"$val.nii.gz
                  fi
              done
              
              ### struct to stand
              if [[ ! -f $dir_func2stand"func2stand_DipHeight.nii.gz" ]]
              then
                echo "struct2stand"
                mkdir $dir_func2stand
                python3 /home/local/VANDERBILT/dolel/Documents/rsHRF/src/py/registration_func2_stand_ants.py --rsfmri ${exp} --atlas ${atlas}
              fi

            fi
            i=$((i+1))
          fi
      fi
    done
  fi
done