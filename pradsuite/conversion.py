#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conversion.py: Conversion between common file formats and common object types

Created by Scott Feister on Mon Feb 22 14:46:03 2021
"""

import astropy.units as u
import numpy as np

from plasmapy.plasma.grids import CartesianGrid

import pradformat as prf

############### PlasmaPy Cartesian Grid Object <----> pradformat Simple Fields File/Object ################
def save_prf_grid(grid, h5filename, label=None, description=None):
    """Save PlasmaPy Grid to pradformat SimpleFields file"""  
    fld = grid2sf(grid, label=label, description=description)
    fld.save(h5filename)

def load_prf_grid(h5filename):
    """Load PlasmaPy Grid from pradformat SimpleFieds file"""
    fld = prf.prad_load(h5filename)
    return sf2grid(fld)
    
def grid2sf(grid, label=None, description=None):
    """
    Creates a pradformat SimpleFields object from a PlasmaPy Cartesian Grid object 
    """
    fld = prf.SimpleFields()
    fld.X = grid.pts0.to(u.m).value
    fld.Y = grid.pts1.to(u.m).value
    fld.Z = grid.pts2.to(u.m).value
    sf_lbls = ["Ex", "Ey", "Ez", "Bx", "By", "Bz"] # Simple Fields attribute labels
    grid_lbls = ["E_x", "E_y", "E_z", "B_x", "B_y", "B_z"] # corresponding PlasmaPy Grids attribute labels
    for sf_lbl, grid_lbl in zip(sf_lbls, grid_lbls):
        if grid_lbl in grid.quantities:
            setattr(fld, sf_lbl, grid[grid_lbl])
        else:
            setattr(fld, sf_lbl, 0.0) # If PlasmaPy Grid attribute is unset, set corresponding Simple Fields attribute value to 0.0
    
    if not isinstance(label, type(None)):
        fld.label = label
        
    if not isinstance(description, type(None)):
        fld.description = description
    
    return fld

def sf2grid(fld):
    """
    Creates a PlasmaPy Cartesian Grid object from a pradformat SimpleFields object
    """
    assert isinstance(fld, prf.SimpleFields)

    grid = CartesianGrid(fld.X*u.m, fld.Y*u.m, fld.Z*u.m)
    
    ones = np.ones(grid.shape)
    # Added "ones" factor to promote any scalar attributes in the SimpleFields file to arrays, and avoid a grids error
    grid.add_quantities(E_x = ones * fld.Ex*u.V/u.m,
                        E_y = ones * fld.Ey*u.V/u.m,
                        E_z = ones * fld.Ez*u.V/u.m,
                        B_x = ones * fld.Bx*u.T,
                        B_y = ones * fld.By*u.T,
                        B_z = ones * fld.Bz*u.T)
    return grid

if __name__ == "__main__":
    pass