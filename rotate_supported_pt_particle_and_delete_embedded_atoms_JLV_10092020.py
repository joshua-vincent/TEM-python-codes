# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:43:33 2020

Tilts are performed on Pt sites about the principle axes of the supercell. 
The anchor point is chosen to be the center of the supercell.

Before running, the user needs to specify (1) the range of tilts to rotate 
the nanoparticle in each axis, and (2) whether to delete Pt embedded in the
support after rotation.

Running the script will first prompt the user to choose a .cif file to load.
This file should be the base file upon which all rotations will be applied.

After 30 seconds or so, the script will prompt the user again to select a directory.
This directory is where all of the files will be saved.

@author: Joshua Vincent, Arizona State University (jvincen5@asu.edu)
"""

## Import necessary modules
import pymatgen as mg
import os
from tkinter import filedialog

## Initiliaze and import base structure from .cif file
#  and determine indices corresponding to Pt
structure_file = os.path.normpath(filedialog.askopenfilename())
structure_name = os.path.splitext(os.path.basename(structure_file))[0] # Base structure name without .cif extension
BaseStructure = mg.IStructure.from_file(structure_file) # Make base structure immutable
BaseStructureDict = BaseStructure.as_dict()
PtIndices = BaseStructure.indices_from_symbol("Pt")

## Choose a directory to save the .cif files after rotating.
save_directory = os.path.normpath(filedialog.askdirectory())

## Specify if you want to delete Pt beneath the CeO2 support surface before saving
DeleteEmbeddedPt = True

## Initialize range of tilts to rotate the nanoparticle in each axis
a_tilts_list = [0, 2, 4] # Amount to tilt about A axis (degrees)
b_tilts_list = [0, 2] # Amount to tilt about B axis (degrees)
c_tilts_list = [0] # Amount to tilt about C axis (degrees)

## Designate an anchor point about which to perform the rotations
#  Here we choose the center of the supercell
anchor = list(0.5*supercell_dimension for supercell_dimension in BaseStructure.lattice.abc)

## Initalize directions of tilt axes
a_axis = [1, 0, 0] # Principle axis for A
b_axis = [0, 1, 0] # Principle axis for B
c_axis = [0, 0, 1] # Principle axis for C

#! The next step of the script is to perform the rotations.
#! Ensure that all inialization above is complete before proceeding.

## Perform rotations on Pt. Rotations are sequentially applied in A, B, and then C directions
for c_tilt in c_tilts_list:
    for b_tilt in b_tilts_list:
        for a_tilt in a_tilts_list:
            RotatedStructure = None
            RotatedStructure = mg.Structure.from_dict(BaseStructureDict) # Copy structure to do the rotations on it instead of the base one.
            
            if a_tilt != 0:
                a_theta = a_tilt*2*3.14159/360 # Convert from degrees to radians
                # Rotate about A axis
                RotatedStructure.rotate_sites(anchor=anchor,axis=a_axis,indices=PtIndices,theta=a_theta,to_unit_cell=True)
                
            if b_tilt != 0:
                b_theta = b_tilt*2*3.14159/360 # Convert from degrees to radians
                # Rotate about B axis
                RotatedStructure.rotate_sites(anchor=anchor,axis=b_axis,indices=PtIndices,theta=b_theta,to_unit_cell=True)
                
            if c_tilt != 0:
                c_theta = c_tilt*2*3.14159/360 # Convert from degrees to radians
                # Rotate about C axis
                RotatedStructure.rotate_sites(anchor=anchor,axis=c_axis,indices=PtIndices,theta=c_theta,to_unit_cell=True)

            # Get file name after rotating
            degrees_tilted = f'{a_tilt:03d}a{b_tilt:03d}b{c_tilt:03d}c'
            rotated_name = structure_name + f'_{degrees_tilted}'
                            
            if DeleteEmbeddedPt:
                # On-going work in progress...
                PtIndices = RotatedStructure.indices_from_symbol("Pt")
                sites_to_remove = []
                for index in PtIndices:
                    if RotatedStructure[index].b < 0.49:
                        sites_to_remove.append(index)
                tuple(sites_to_remove)
                RotatedStructure.remove_sites(sites_to_remove)
                rotated_name += '_NoBuriedPt'
                        
            # Save .cif file with rotated Pt atoms to the save directory
            save_filename = os.path.join(save_directory, rotated_name + '.cif')
            RotatedStructure.to(filename=save_filename)