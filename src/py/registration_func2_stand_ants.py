import ants
import os 
import argparse
import numpy as np

def main(args):
  params = [ 'DipHeight', 'TroughHeight', 'Time2dip', 'Time2trough', 'PeakIntegral', 'DipIntegral', 'TroughIntegral', 'Olrm_Height', 'Olrm_FWHM', 'Olrm_Time2peak']
  subject_dir = args.rsfmri_dir

  ## atlas
  stand = ants.image_read(args.atlas)

  ## T1 file
  anat_file =os.path.join(subject_dir, 'anat/T1.nii.gz')
  anat = ants.image_read(anat_file)

  ## struct_dir 
  struct_dir = os.path.join(subject_dir, 'func2struct')

  ## stand_dir 
  stand_dir = os.path.join(subject_dir, 'func2stand')



  ### 1st step  structural to standard registration
  struct2stand = ants.registration(fixed=stand, moving=anat, type_of_transform="SyN")

  ### 2nd step apply transform
  func2stand = struct2stand['fwdtransforms']
  prefix = 'func2struct_'
  
  for param in params:
    name = prefix + param + '.nii.gz'
    file= os.path.join(struct_dir, name)
    struct = ants.image_read(file)
    warpimage = ants.apply_transforms(fixed=stand, moving=struct, transformlist=func2stand)

    outname= 'func2stand_' + param + '.nii.gz'
    output=os.path.join(stand_dir,outname)
    ants.image_write(warpimage, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--rsfmri_dir', type=str)
    parser.add_argument('--atlas', type=str)
  
    args = parser.parse_args()

    main(args)
