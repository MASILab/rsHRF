#!/bin/bash
folder='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/ADNI_23/'
atlas='/home/local/VANDERBILT/dolel/Documents/rsHRF_project/atlases/mni_icbm152_nlin_asym_09c/mni_icbm152_t1_tal_nlin_asym_09c.nii'
# i=32
i=0
cd $folder
for subject in * ; do
 if [ -d "$subject" ]; then
  subject_dir="${folder}${subject}/"
  cd $subject_dir
   for exp in * ]; do
    if [ -d  "${exp}/rsfmri" ] ; then
     if [[ "$i" -ge 0 ]]; then
        exp_dir="${subject_dir}${exp}/"

        cd $exp_dir

        # func_dir='rsfmri'
        # T1="anat/T1_copy.nii.gz"

        # dir_func2stand="func2standard/"

        echo $i  "-----${subject_dir}${exp}------"
        cd ..
        # echo $i

        # height= 'rsfmri/Deconv_Detrend_4DVolume_Olrm_Height.nii')
        # params = ['Olrm_Height', 'Olrm_FWHM', 'Olrm_Time2peak', 'Time2dip', 'DipHeight', 'PeakIntegral', 'DipIntegral']  

        # stand = ants.image_read(args.atlas)
        # struct = ants.image_read(args.T1)
        # func = ants.image_read(height)

        # ### 1st step  structural to standard registration
        # # struct2stand = antsRegistration(fixed=stand, moving=struct, type_of_transform="SyN")
        # ./antsRegistration --


        # ### 2nd step : FSL-ANTs transform conversion - functional to structural
        # matfile = os.path.join(args.dir_func2struct, 'func2struct_Height.mat')

        # # read fsl affine transform and save it as ants affine transform
        # mat_func2struct = np.loadtxt(matfile)
        # mat = ants.fsl2antstransform(mat_func2struct, struct, func)
        # out_matfile = os.path.join(args.dir_func2struct, 'func2struct_Height_ants.mat')
        # ants.write_transform(mat, out_matfile)

        # # apply func2struct ants affine transform to save the corresponding warp image
        # func2struct_warped = ants.apply_transforms(fixed=struct, moving=func, transformlist=out_matfile)
        # out_warp_imgfile =  os.path.join(args.dir_func2struct, 'func2struct_Height_warp_ants.nii.gz')
        # ants.image_write(func2struct_warped,out_warp_imgfile)

        # # create the func2struct ants transform list to concatenate to struct2stand list
        # func2struct = [ out_matfile, out_warp_imgfile]



        # ### 3rd step: Concatenate transforms in one transform: functional to structural

        # func2stand = func2struct + struct2stand['fwdtransforms']

        # prefix = 'Deconv_Detrend_4DVolume_'
        # for param in params:
        # name = prefix + param + '.nii'
        # file= os.path.join(in_dir, name)
        # func = ants.image_read(file)
        #     warpimage = ants.apply_transforms(fixed=stand, moving=func, transformlist=func2stand)

        #     outname= 'func2stand_' + param + '.nii.gz'
        #     output=os.path.join(out_dir,outname)
        #     ants.image_write(warpimage, output)






     fi
     i=$((i+1))
    fi
   done
  cd ..
  fi
done

# curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
# distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
# curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
# sudo apt-get update
# sudo apt-get install -y nvidia-docker2