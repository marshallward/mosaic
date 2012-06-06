#!/usr/bin/env python
# coding: utf-8

import netCDF4 as nc
import numpy as np
import sys
import argparse

grid_version = '0.2'
code_version = '$Name: siena_201203 $'

"""
Emulation of make_vgrid.c
Contact:    Marshall Ward (marshall.ward@anu.edu.au)
"""

def save(zeta, grid_name=None):
    
    history = ' '.join(sys.argv)
    
    # Default tags
    if not grid_name:
        grid_name = 'vertical_grid.nc'
    
    # Create output file
    vgrid_nc = nc.Dataset(grid_name, 'w')
    
    # Global attributes
    vgrid_nc.grid_version = grid_version
    vgrid_nc.code_version = code_version
    vgrid_nc.history = history
    
    vgrid_nc.createDimension('nzv', nzv)
    
    zeta_nc = vgrid_nc.createVariable('zeta', 'f8', ('nzv',))
    zeta_nc[:] = zeta
    zeta_nc.standard_name = 'vertical_grid_vertex'
    zeta_nc.units = 'meters'

    vgrid_nc.close()
