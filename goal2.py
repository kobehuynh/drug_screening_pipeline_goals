"""
Goal 2: 
Module for computing the 3D coordinates of a fixed cuboid centered at the mean coordinates of specified amino acids from a PDB file.
 
This module uses the BioPython package to parse PDB files and compute the fixed cuboid 
either by considering only alpha carbons, side chain atoms, or considering all atoms in specified residues.
Also, numpy is used to perform the necessary calculations.

Dependencies include:
-Biopython
-numpy
"""

#Import packages

from Bio.PDB import *  
import numpy as np

def get_coord_cuboid_center(pdb_file, amino_acids=None, mean_coord_type = "all_atoms", cuboid_dimensions = []):

    """
    Compute the coordinates of the 3D bounding cuboid for a set of amino acids in a PDB file given a list of dimensions (x,y,z lengths of cuboid
    or a cube if just one length is given) 

    Parameters:

    pdb_file: str
        Path to pdb file to be analyzed.

    amino_acids: list[str], optional, default=None  
        List of amino acid residue names (3-letter codes, e.g, "ALA", "GLY") to be analyzed.
        If None, all residues are analyzed.

    mean_coord_type : str, optional, default="all_atoms"
        The type of atomic coordinates to use for calculating the center of the cuboid. 
        Valid options are:
        - "alpha_carbons": Use only the α-carbon atom coordinates.
        - "all_atoms": Use coordinates from all atoms in the amino acids.
        - "side_chain_atoms": Use coordinates from side-chain atoms only (excludes backbone atoms: CA, O, N, and C).
        
    cuboid_dimensions : list
        A list of three positive values representing the cuboid's lengths along the x, y, and z axes.
        If a single value is provided, a cube is assumed with equal lengths for all axes.

    Output:
    Coordinates of the cuboid:
    -Xmax, Ymax, Zmax: float   
    -Xmin, Ymin, Zmin: float

    Example:
    get_coord_cuboid_center("example.pdb", amino_acids=["ALA", "GLY"], mean_coord_type = "side_chain_atoms", cuboid_dimensions = [10,12,14])

    """
    
    #Check that the mean coordinate type is valid
    valid_coord_types = ["alpha_carbons","all_atoms","side_chain_atoms"]
    if mean_coord_type not in valid_coord_types:
        raise ValueError("Invalid coordinate type entered. Please enter one of the following:" "alpha_carbons", "all_atoms", "side_chain_atoms")

    #Check that the cuboid dimensions are valid
    if cuboid_dimensions is None:
        raise ValueError("You must enter values for cuboid dimensions")
    #If only one value is entered, assume that the cuboid is a cube
    if len(cuboid_dimensions) == 1:
        cuboid_dimensions = np.array([cuboid_dimensions[0]] * 3)
    elif len(cuboid_dimensions) != 3:
        raise ValueError("Incorrect number of values for cuboid dimensions")
    else:
        cuboid_dimensions = np.array(cuboid_dimensions)

    #Load and parse the structure from the PDB file
    parser = PDBParser(PERMISSIVE=1)
    structure = parser.get_structure("protein", pdb_file)

    #Initialize an empty list to store the 3D atom coordinates
    coord = []

    #Iterate over the structure (models, chains, residues) to extract the atom coordinates
    for model in structure:
        for chain in model: 
            for residue in chain:
                if amino_acids is None or residue.resname in amino_acids:
                    for atom in residue:
                        if mean_coord_type == "alpha_carbons":
                            if atom.name == "CA":
                                coord.append(atom.coord)
                        elif mean_coord_type == "all_atoms":
                            coord.append(atom.coord)  
                        elif mean_coord_type == "side_chain_atoms": 
                            if atom.name not in ("CA","O","N","C"):
                                coord.append(atom.coord)

    #Convert the list of coordinates to a numpy array for easier manipulation
    coord_numpy = np.array(coord)

    #Compute the mean coordinates of the specified atoms
    x_mean,y_mean,z_mean = np.mean(coord_numpy, axis=0) 

    #Compute the coordinates of the cuboid
    x_max = x_mean + cuboid_dimensions[0]/2
    x_min = x_mean - cuboid_dimensions[0]/2
    y_max = y_mean + cuboid_dimensions[1]/2
    y_min = y_mean - cuboid_dimensions[1]/2
    z_max = z_mean + cuboid_dimensions[2]/2
    z_min = z_mean - cuboid_dimensions[2]/2

    #Return fixed cuboid coordinates
    return("Xmax=",x_max,"Ymax=",y_max,"Zmax=",z_max,"Xmin=",x_min,"Ymin=",y_min, "Zmin=",z_min)
    