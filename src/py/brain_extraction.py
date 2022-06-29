import ants
import antspynet
import os
import argparse

def main(args):
    # input_dir='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/ADNI_23' 
    input_dir = args.in_dir

    list_sub = sorted(os.listdir(input_dir))
    for subject in list_sub:
        print("subject: ", subject)
        subject_dir = os.path.join(input_dir, subject)
        for experiment in sorted(os.listdir(subject_dir)):
            exp_dir = os.path.join(subject_dir, experiment)

            anat_dir = os.path.join(exp_dir, 'anat')
            if os.path.isdir(anat_dir):
                filename = os.path.join(anat_dir, 'T1_copy.nii.gz')
                out = os.path.join(anat_dir, 'brain_masked.nii.gz')

                img=ants.image_read(filename)
                brain_mask = antspynet.utilities.brain_extraction(img, modality='t1')
                brain_mask = ants.threshold_image(brain_mask, 0.5, 1, 1, 0)
                brain_mask = ants.morphology(brain_mask,"close",6).iMath_fill_holes()

                brain_masked=brain_mask*img
                ants.image_write(brain_masked, out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Display ComBAT results')
    
    
    ## input
    input = parser.add_argument_group('input arguments')
    input.add_argument('--in_dir', type=str, help='input directory containing dataset', required=True)

    args = parser.parse_args()
    main(args)
