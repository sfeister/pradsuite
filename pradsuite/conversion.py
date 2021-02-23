#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
conversion.py: Conversion between common file formats and common object types

Created by Scott Feister on Mon Feb 22 14:46:03 2021
"""

import astropy.units as u
import numpy as np

from plasmapy.plasma.grids import CartesianGrid
from plasmapy.diagnostics.proton_radiography import SyntheticProtonRadiograph
from plasmapy.particles import Particle

import pradformat as prf
from pradformat import SimpleFields, SimpleRadiograph, ParticlesList

############### PlasmaPy Cartesian Grid Object <----> pradformat Simple Fields File/Object ################
def grid2prf(grid : CartesianGrid, h5filename, label=None, description=None):
    """Save PlasmaPy Grid to pradformat SimpleFields file"""  
    fld = grid2sf(grid, label=label, description=description)
    fld.save(h5filename)

def prf2grid(h5filename):
    """Load PlasmaPy Grid from pradformat SimpleFieds file"""
    fld = prf.prad_load(h5filename)
    return sf2grid(fld)
    
def grid2sf(grid : CartesianGrid, label=None, description=None):
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

def sf2grid(fld : SimpleFields):
    """
    Creates a PlasmaPy Cartesian Grid object from a pradformat SimpleFields object
    """
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

#### PlasmaPy Synthetic Proton Radiography Object's Particles ----> pradformat Particles List ############
def sradparts2prf(sim : SyntheticProtonRadiograph, h5filename, label=None, description=None):
    """Save PlasmaPy Synthetic Proton Radiograph particles to pradformat ParticlesList file"""  
    plist = sradparts2plist(sim, label=label, description=description)
    plist.save(h5filename)

def sradparts2plist(sim : SyntheticProtonRadiograph, label=None, description=None):
    """
    Creates a pradformat ParticlesList object from a PlasmaPy SyntheticRadiograph object 
    """
    assert sim.nparticles > 1

    plist = prf.ParticlesList()
    plist.charge = sim.q
    plist.mass = sim.m
    plist.x = sim.x[:,0]
    plist.y = sim.x[:,1]
    plist.z = sim.x[:,2]
    plist.px = sim.m * sim.v[:,0]
    plist.py = sim.m * sim.v[:,1]
    plist.pz = sim.m * sim.v[:,2]
    plist.energy = sim.proton_energy
    
    if not isinstance(label, type(None)):
        plist.label = label
        
    if not isinstance(description, type(None)):
        plist.description = description
    
    return plist

if __name__ == "__main__":
    pass