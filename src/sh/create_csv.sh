#!/bin/bash

Help()
{
# Display Help
echo "Help"
echo "Create csv file from dataset"
echo
echo "Syntax: create_csv.sh [--options]"
echo "options:"
echo "--input_dir           Input directory containing features csv files "
echo "--csv             Output directory"

}

## works for ComBAT.py, age_csv.py
while [ "$1" != "" ]; do
    case $1 in
        --in_dir )  shift
            in_dir=$1;;
        --out_csv )  shift
            out_csv=$1;;
        -h | --help )
            Help
            exit;
    esac
    shift
done

echo $in_dir
echo subject_dir, fmri >> $out_csv

i=0
for subject in $in_dir* ; do
 if [ -d "$subject" ]; then
   for exp in $subject/* ; do
    test=$exp/rsfmri/Detrend_4DVolume.nii
    if [ -f $test ]; then
        i=$((i+1))
        echo $exp , rsfmri/Detrend_4DVolume.nii >> $out_csv
    fi
   done
  fi
done