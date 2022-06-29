import ants
import os 
import argparse
import numpy as np

def main(args):

  out_dir = args.func2stand
  in_dir = args.rsfmri_dir

  # height= os.path.join(in_dir, 'func2structHeight.nii.gz')  
  
  params = ['Time2trough', 'TroughHeight', 'TroughIntegral', 'PeakIntegral_v2', 'DipIntegral_v2']  
  
  stand = ants.image_read(args.atlas)
  struct = ants.image_read(args.T1)
  # func = ants.image_read(height)
  
  ### 1st step  structural to standard registration
  struct2stand = ants.registration(fixed=stand, moving=struct, type_of_transform="SyN")



  ### 2nd step : FSL-ANTs transform conversion - functional to structural
  # matfile = os.path.join(args.dir_func2struct, 'func2struct_Height.mat')

  # # read fsl affine transform and save it as ants affine transform
  # mat_func2struct = np.loadtxt(matfile)
  # mat = ants.fsl2antstransform(mat_func2struct, struct, func)
  # out_matfile = os.path.join(args.dir_func2struct, 'func2struct_Height_ants.mat')
  # ants.write_transform(mat, out_matfile)

  # apply func2struct ants affine transform to save the corresponding warp image
  # func2struct_warped = ants.apply_transforms(fixed=struct, moving=func, transformlist=out_matfile)
  # out_warp_imgfile =  os.path.join(args.dir_func2struct, 'func2struct_Height_warp_ants.nii.gz')
  # ants.image_write(func2struct_warped,out_warp_imgfile)

  # create the func2struct ants transform list to concatenate to struct2stand list
  # func2struct = [ out_matfile, out_warp_imgfile]  ### 3rd step: Concatenate transforms in one transform: functional to structural

  func2stand = struct2stand['fwdtransforms']

  prefix = 'func2struct_'
  
  for param in params:
    name = param + '/' + prefix + param + '.nii.gz'
    file= os.path.join(in_dir, name)
    func = ants.image_read(file)
    warpimage = ants.apply_transforms(fixed=stand, moving=func, transformlist=func2stand)

    outname= 'func2stand_' + param + '.nii.gz'
    output=os.path.join(out_dir,outname)
    ants.image_write(warpimage, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--T1', type=str)
    parser.add_argument('--rsfmri_dir', type=str)
    # parser.add_argument('--dir_func2struct', type=str)

    parser.add_argument('--atlas', type=str)
    parser.add_argument('--func2stand', type=str)
  
    args = parser.parse_args()

    main(args)
