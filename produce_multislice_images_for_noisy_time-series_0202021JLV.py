# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 12:23:00 2021

@author: Josh
"""

#%% 1.1) Import modules and set constants

# Import important modules
import drprobe as drp
import numpy as np
import os
import shutil
import sys
from PIL import Image
from random import randint
from tkinter import filedialog

# Initialize constant parameters
ht = 300;                   # High tension is 300 kV
nx = 512; ny = 512;         # All images, wavefunctions, etc. will be nx x ny pixels
nz = 300;                   # The structures will be cut into 300 slices
dwf = True; buni = 0.005;   # Debye-Wallar factor on and set B = 0.5 Ang^2
absorb = True;              # Apply built-in absorptive form factors
output = True;              # Give chatty output during simulations
Cs = -9000                 # Cs = -9 um
C5 = 5000000                # C5 = 5 mm

#%% 1.2) Specify input and output directories

# Input directory containing .cel files to be simulated
print('Select an input directory containing .cel files to be simulated')
input_dir = os.path.normpath(filedialog.askdirectory())

# Output directory where in-progress simulations should be saved
print('Select an output directory where in-progress simulations should be saved')
output_dir = os.path.normpath(filedialog.askdirectory())
# output_check_dir = os.path.join(output_dir, 'SimulationCheck')
# try:
#     os.mkdir(output_check_dir)
# except:
#     print("Did not make check directory")

# Image directory where all the clean simulated images should be saved
print('Select a directory where all final simulated images will be saved')
clean_image_dir = os.path.normpath(filedialog.askdirectory())

# Directory where all the noisy simulated images should be saved
print('Select a directory where the noisy images will be saved')
noisy_image_dir = os.path.normpath(filedialog.askdirectory())

# Range of defocus in nm. Positive values indicate overfocus
defoci = [8]

# Range of vacuum levels in terms of electron counts
vac_levels = [1, 4, 16]
for vac_level in vac_levels:
    os.mkdir(os.path.join(noisy_image_dir, f'vac_int-{vac_level:02d}counts'))

# Read lattice parameters from cel file
a, b, c = np.genfromtxt(r'G:\SimMovies\data\raw\atom_hopping_RhCeO2_20210122\seq_structures_cel\RhCeO2_seq0000_adatom_CN-5.cel', skip_header=1, skip_footer=1, usecols=(1, 2, 3))[0]

#%% 1.3a) Option A: Initialize Parameter Files from Scratch

# Directory where initialized parameter files should be saved
prm_dir = r'G:\SimMovies\data\raw\atom_hopping_RhCeO2_20210122\init_prm'

# Initialize general MSA Parameter File
msa_prm_gen = drp.msaprm.MsaPrm()
msa_prm_gen.wavelength = 0.0019687482               # Electron wavelength in nm
msa_prm_gen.focus_spread = 4                        # Focus half-spread in nm
msa_prm_gen.h_scan_frame_size = a                   # This is the size of the cel in nm
msa_prm_gen.v_scan_frame_size = b 
msa_prm_gen.tilt_x = 2                              # Tilt of crystal in x direction (degrees)
msa_prm_gen.tilt_y = -1                             # Tilt of crystal in y direction (degrees)
msa_prm_gen.scan_columns = nx                       # Unsure if matters but consistent with image
msa_prm_gen.scan_rows = ny  
msa_prm_gen.temp_coherence_flag = 0                 # Turn off temporal coherence calculation (STEM only)
msa_prm_gen.spat_coherence_flag = 0                 # Turn off spatial coherence calculation (STEM only)
msa_prm_gen.slice_files = ''                        # String of slice file, will be set iteratively later
msa_prm_gen.number_of_slices = nz                   # Load one slice at a time
msa_prm_gen.det_readout_period = 0                  # No detector effects included.
msa_prm_gen.tot_number_of_slices = nz               # Each structure contains 155 slices
msa_prm_gen.aberrations_dict = {1: (0, 0),          # Defocus of 0 nm standard, will be adjusted iteratively later
                                5: (Cs, 0),         # Cs = -13 um
                                11: (C5, 0)}        # C5 = 5 mm         
# Save the initailized MSA prm file
msa_prm_gen.save_msa_prm(prm_dir + r'\MsaPrmN2PtNP_Initialized.prm') 

# Initialize general WavImg Parameter File
wav_prm_gen = drp.wavimgprm.WavimgPrm()
wav_prm_gen.high_tension = ht                       # Set HT to 300 kV
wav_prm_gen.wave_dim = (nx, ny)                     # Pixel dimensions of wave are nx by ny
wav_prm_gen.wave_sampling = (a/nx, b/ny)            # Pixel size is width of cell divided by pixel dimensions
wav_prm_gen.output_format = 0                       # Output TEM image
wav_prm_gen.output_dim = (nx, ny)                   # Pixel dimensions of image are nx by ny
wav_prm_gen.coherence_model = 1                     # Explicit TCC calculation
wav_prm_gen.temp_coherence = (1,4)                  # Turn on temporal coherence. Focal spread half-width of 4 nm
wav_prm_gen.spat_coherence = (1,0.2)                # Turn on spatial coherence. Beam convergence half angle of 0.2 mrad
wav_prm_gen.mtf = (0, 1, r'E:\MTF-US2k-300.mtf')    # Turn off detector MTF effect. Calculation scale of the mtf = (sampling rate experiment)/(sampling rate simulation)
wav_prm_gen.vibration = (1, 0.05, 0.05, 0)          # 50 pm isotropic vibration applied.
wav_prm_gen.oa_radius = 250                         # Objective aperture essentially out, set to 250 mrad
wav_prm_gen.aberrations_dict = {1: (0, 0),          # Defocus of 0 nm standard, will be adjusted iteratively later
                                5: (Cs, 0),         # Cs = -13 um
                                11: (C5, 0)}        # C5 = 5 mm    
wav_prm_gen.save_wavimg_prm(prm_dir + r'\WavPrmN2PtNP_Initialized.prm') # Save the initailized WavImg prm file)

#%% 1.3b) Option B: Initialize Parameter Files from Previously Saved Files

# Load MSA parameter file
msa_prm_gen = drp.msaprm.MsaPrm()
print('Specify a MSA parameter file to use during the simulations')
msa_prm_gen.load_msa_prm(os.path.normpath(filedialog.askopenfilename()))

# Load WAV parameter file
wav_prm_gen = drp.wavimgprm.WavimgPrm()
print('Specify a WAV parameter file to use during the simulations')
wav_prm_gen.load_wav_prm(os.path.normpath(filedialog.askopenfilename()))

#%% 2) Perform Image Simulations

# For every structure in the input directory
for cel_file in os.listdir(input_dir):
   
    ## Set-up parent directory for this structure
    # Remove the file extension to isolate the structure name
    structure_name = cel_file[:-4]
    # Name of directory for this structure, to be within the output directory
    structure_dir = os.path.join(output_dir, structure_name)     
    # Create structure's directory with name specified above       
    os.mkdir(structure_dir)

    ## 2.1) Create back-up of cel file in output directory
    
    # Set-up cel sub-directory
    structure_cel_dir = os.path.join(structure_dir, 'cel')
    # Create cel directory with name specified above
    os.mkdir(structure_cel_dir)
    # Name of full directory to original cel file
    cel_original = r'"{}"'.format(os.path.join(input_dir, cel_file))
    # The r'"{}"' formatting is necessary to enclose the path in double quotes.
    cel_copy = r'"{}"'.format(os.path.join(structure_cel_dir, cel_file))
    # Create back-up cel in back-up directory
    drp.commands.cellmuncher(cel_original, cel_copy, output=True)                                      
    
    ## 2.2) Slice cel and save slices in \slc directory
    # Set-up slice sub-directory
    structure_slc_dir = os.path.join(structure_dir, 'slc')
    os.mkdir(structure_slc_dir)
    slice_name = structure_name + '_slc'
    slice_path_and_name = os.path.join(structure_slc_dir,slice_name)
    
    # Slice cel and save slices in the slice directory
    drp.commands.celslc(cel_original, slice_path_and_name,                      
                        ht, nx, ny, nz, 
                        absorb=absorb, dwf=dwf, buni=buni, 
                        output=True)
    
    
    ## 2.3) Perform multislice simulation
    # Parameter initialization
    # Set up name of parameter (or 'prm') sub-directory for this structure
    structure_prm_dir = os.path.join(structure_dir, 'prm')
    # Create parameter directory with name specified above
    os.mkdir(structure_prm_dir)
    # Load general parameter file to be edited
    msa_prm = msa_prm_gen
    # Specify location of phase gratings generated in section 2.2
    msa_prm.slice_files = slice_path_and_name
    # Name the MSA parameter file to be saved
    msa_prm_name = 'MsaPrm_'+structure_name+'.prm'
    # Path location to where the MSA parameter file should be saved 
    msa_prm_path_and_name = os.path.join(structure_prm_dir, msa_prm_name)
    # Save the parameter file with the slice locations
    msa_prm.save_msa_prm(msa_prm_path_and_name)
    
    ## Set-up wave function sub-directory
    # Set up name of wave function (or 'wav') sub-directory for this structure
    structure_wav_dir = os.path.join(structure_dir, 'wav')
    # Create wave function directory with name specified above
    os.mkdir(structure_wav_dir)
    # Specify name (and path) of output wavefunction
    wav_path = os.path.join(structure_wav_dir,structure_name)
    
    # Calculate exit surface wavefunction and save it in wav_path
    drp.commands.msa(msa_prm_path_and_name, wav_path,
                     ctem = True, output = True, 
                     silent = False)
    
    
    ## 2.4) Generate simulated images
    # Parameter initialization
    # Load general wav parameter file for image simulation
    wav_prm = wav_prm_gen
    # Name of wave file and location after full multislice simulation
    wav_prm.wave_files = wav_path + '_sl' + f'{nz:03d}' + '.wav'
    # Set name of wave paramter file
    wav_prm_name = 'WavPrm_'+structure_name+'.prm'
    # Path location to where the wav parameter file should be saved
    wav_prm_path_and_name = os.path.join(structure_prm_dir, wav_prm_name)
    # Save the parameter file with the slice locations
    wav_prm.save_wavimg_prm(wav_prm_path_and_name)
    
    ## Set-up image sub-directory
    # Set up name of image (or 'img') sub-directory for this structure
    structure_img_dir = os.path.join(structure_dir, 'img')                     
    # Create image  directory with name specified above
    os.mkdir(structure_img_dir)
    
    # Simulate images
    for defocus in defoci:
            # Specify name (img_name) of path (output_img) of output image
            img_name = structure_name+'_'+str(nz)+'slc_'+str(nx)+'x'+str(ny)+'_'+str(defocus)+'nmDefocus'+'.dat'
            output_img = os.path.join(structure_img_dir,img_name)
            
            # Calculate image
            drp.commands.wavimg(wav_prm_path_and_name, output_img, 
                                foc = defocus,
                                sil = False, output=True)
            
            # Save the clean image as a tif file
            clean_img_array = np.fromfile(output_img, dtype=np.single).reshape((nx, ny))
            clean_img_array = np.flip(clean_img_array,0)
            clean_img = Image.fromarray(clean_img_array) 
            clean_img.save(os.path.join(clean_image_dir, img_name[:-4] + '.tif'))
            
            # Save a noise realizations of the image
            for vac_level in vac_levels:
                noisy_img_array = np.random.poisson(clean_img_array*vac_level)
                noisy_img = Image.fromarray(noisy_img_array) 
                noisy_img.save(os.path.join(noisy_image_dir, 
                                            f'vac_int-{vac_level:02d}counts',
                                            img_name[:-4] 
                                            + f'_noisy_vac_int-{vac_level:02d}counts.tif'
                                            )
                               )
            
            # Save every 1 in 10 images randomly for diagnostics
            # if randint(0,100) > 90:
            #     shutil.copyfile(output_img, os.path.join(output_check_dir,img_name))
    
    ## 2.5) Clean up slice directory
    # Delete slice sub-directory to save space
    try:
        shutil.rmtree(structure_slc_dir)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
