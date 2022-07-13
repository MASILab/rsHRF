#!/bin/bash

Help()
{
# Display Help
echo "Help"
echo "Run scripts for each HRF feature"
echo
echo "Syntax: apply_py_parameters.sh [--options]"
echo "options:"
echo "--input_dir           Input directory containing features csv files "
echo "--output_dir          Output directory"
echo "--py_file             python script to apply on each feature"

}

## works for ComBAT.py, age_csv.py
params="Height DipHeight TroughHeight PeakIntegral DipIntegral TroughIntegral Time2peak Time2dip Time2trough FWHM"

while [ "$1" != "" ]; do
    case $1 in
        --in_dir )  shift
            input_dir=$1;;
        --out_dir )  shift
            output_dir=$1;;
        --py_file )  shift
            py_file=$1;;
        -h | --help )
            Help
            exit;
    esac
    shift
done

## input parameters to .sh
age_subject='../../../rsHRF_project/list_params_subject_experiment_v3.csv' 
# TR_subject='../../../rsHRF_project/txt/list_TR_scans.csv'
scanner='../../../rsHRF_project/txt/infos_site_subjects.csv'

echo $in_dir
input_dir=../../../rsHRF_project/output/WM_GM_analysis/csv_cleaned/
output_dir=../../../rsHRF_project/output/WM_GM_analysis/csv_harmonized/Model_and_TR/
# Iterate the string variable using for loop
for val in $params; do
    in_file=$input_dir$val'_canonical_regcleaned.csv'
    out_csv=$output_dir$val'_canonical.csv'
    python3 $py_file --in_csv $in_file --out_csv $out_csv ## comBAT
    # python3 $py_file --csv_to_age $in_file --outfile $out_csv --csv_age_subject $age_subject --csv_site $scanner
done