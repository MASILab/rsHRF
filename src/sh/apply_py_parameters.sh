#!/bin/bash

Help()
{
# Display Help
echo "Help"
echo "Run scripts for each HRF feature"
echo
echo "Syntax: apply_py_parameters.sh [--options]"
echo "options:"
echo "--in_dir           Input directory containing features csv files "
echo "--out_dir          Output directory"
echo "--py_file             python script to apply on each feature"

}

## works for ComBAT.py, age_csv.py
params="Height DipHeight TroughHeight Time2peak Time2dip Time2trough FWHM PeakIntegral DipIntegral TroughIntegral"

while [ "$1" != "" ]; do
    case $1 in
        --in_dir )  shift
            in_dir=$1;;
        --py_file )  shift
            py_file=$1;;
        --out_dir )  shift
            out_dir=$1;;
        -h | --help )
            Help
            exit;
    esac
    shift
done

## input parameters to .sh
# age_subject='../../../rsHRF_project/txt/list_params_subject_experiment_v3.csv' 
# scanner='../../../rsHRF_project/txt/infos_site_subjects.csv'


age_subject='../../../rsHRF_project/txt/ADNI_BLSA_infos.csv'

# Iterate the string variable using for loop
for val in $params; do
    in_file=${in_dir}$val".csv"
    out_csv=${out_dir}$val".csv"
    python3 $py_file --in_csv $in_file --out_csv $out_csv --rois 48 2 ## comBAT
    # python3 $py_file --csv_to_age $in_file --outfile $out_csv --csv_age_subject $age_subject 
done