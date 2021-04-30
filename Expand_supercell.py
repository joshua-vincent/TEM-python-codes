"""
Created on Thu Apr 8, 12:40 PM, 2021

Expands supercell of  model by specifed amount uniformly from model center.
This is useful to do prior to rotating a model in order to provide some
padding around the model edges to avoid boundary artifacts during a 
multislice TEM image simulation.

Before running, the user needs to specify (1) the expansion factor, i.e.,
a scaling factor to specify how much to expand the supercell dimensions,
(2) a directory where the expanded supercell structure model will be saved,
and (3) the minimum supercell dimension after expansion. The script will 
expand the model dimensions by the expansion factor, and if this expanded
distance lies below the minimum specified threshold, the threshold distance 
will be chosen as the supercell dimension instead.

The 'pymatgen', 'os', and 'tkinter' packages are required.

@author: Joshua Vincent, Arizona State University (jvincen5@asu.edu)
"""

## Import necessary modules
import pymatgen as mg
import os
from tkinter import filedialog

## Specify expansion factor. Setting equal to 1 results in no change.
expansion_factor = 1.20

## Specify minimum supercell dimension, in Angstroms.
# If the expanded distance is less than this minimum, the dimension
# will be set as this minimum value instead.
min_dimension = 15

## Specify save directory
print("Please specify a directory in which to save the expanded .cif file:")
save_directory = os.path.normpath(filedialog.askdirectory())

## Initiliaze and import original structure from a .cif file
print("Please choose a .cif file that you would like to expand:")
structure_file = os.path.normpath(filedialog.askopenfilename())
structure_name = os.path.splitext(os.path.basename(structure_file))[0]
OriginalStructure = None
OriginalStructure = mg.IStructure.from_file(structure_file)

## Create ExpandedStructure with larger supercell
ExpandedStructure = None
# Calculate expanded supercell dimension
abc = list(round(expansion_factor * lattice_param, 3) 
           for lattice_param in OriginalStructure.lattice.abc)
# If expanded dimension is less than minimum, set dimension equal to minimum
abc = [lattice_param if lattice_param > min_dimension 
       else min_dimension for lattice_param in abc]
latt = mg.Lattice.from_parameters(abc[0], abc[1], abc[2], 90, 90, 90)
# Create expanded structure object. 
# One 'dummy' site (to be deleted) is necessary to initialize the object.
ExpandedStructure = mg.Structure(latt, ["O"], [[0,0,0]])
# Remove dummy site
ExpandedStructure.remove_sites([0])

## Add every site from OriginalStructure
for site in OriginalStructure:  
    ExpandedStructure.append(site.specie, 
                             site.coords, 
                             coords_are_cartesian=True)

# Translate all sites by a distance equal to 
# half of the expansion distance in each axis
translation_vector = [0.5*(new_lat_param - old_lat_param) 
                      for new_lat_param, old_lat_param 
                      in zip(abc, OriginalStructure.lattice.abc)]
ExpandedStructure.translate_sites(list(range(ExpandedStructure.num_sites)), 
                                  translation_vector, 
                                  frac_coords=False)

# Save ExpandedStructure as .cif file
expanded_name = structure_name + '_expanded'
save_filename = os.path.join(save_directory, expanded_name + '.cif')
ExpandedStructure.to(filename=save_filename)