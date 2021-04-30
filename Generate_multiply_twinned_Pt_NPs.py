"""
Created on Fri Apr 30 11:32:50 2021

Generates multiply twinned Pt nanoparticles.
The 'wulffpack' and 'ase' packages are required.
A twinned nanoparticle of a specified size will be written to an .xyz file.

@author: Joshua Vincent, Arizona State University (jvincen5@asu.edu)
"""

# Import necessary modules
from wulffpack import Decahedron
from ase.build import bulk
from ase.io import write

# Specify (relative) surface energies of Pt 
surface_energies = {(1, 0, 0): 2.036,
                    (1, 1, 1): 2.0,
                    (1, 1, 0): 2.5}

# Produce primitive structure from Pt lattice parameter (3.912 Angstroms)
prim = bulk('Pt', a=3.912)

# Produce a twinned particle using the Decahedron function
# A default relative twin energy of 0.04 is used
particle = Decahedron(surface_energies,
                      twin_energy=0.04,
                      primitive_structure=prim)

# Specify the size (number of atoms) of the twinned particle
particle.natoms = 325

# Write the twinned particle structure to an .xyz format file
# A file name will need to be provided where "Filename" is written
write('Filename.xyz', particle.atoms)