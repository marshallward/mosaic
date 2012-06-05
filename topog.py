#!/usr/bin/env python
# coding: utf-8

import netCDF4 as nc
import numpy as np
import sys

grid_version = '0.2'
code_version = '$Name: siena_z1l $'

"""
Emulation of make_topog.c
"""
def main():

    # Testing parameters
    grid_file = 'horizontal_grid.nc'
    
    grid_nc = nc.Dataset(grid_file, 'r')
    x_grid = grid_nc.variables['x'][1::2, 1::2]
    y_grid = grid_nc.variables['y'][1::2, 1::2]
    
    # Testing
    x = x_grid[0,:]
    y = y_grid[:,0]
   
    nx = x.size
    ny = y.size

    depth = np.zeros([ny, nx])
    depth = andy_topog(x_grid, y_grid)
    
    save_topog(depth)


def example_topog(x, y):
    """
    Example of a complex depth function
    Created by Andy Hogg for MITgcm sector modelling
    """
    
    # Arbitrary parameters
    D = 4000.
    dc = 59.
    nx = x.shape[1]
    rx = 0.25   # Base resolution
    shelf_depth = 800.
    sws = 3.
    dy_end = 0.5*(y[-2,0] - y[-1,0])
    y_end = y[-1,0] + dy_end
    
    # Western shelf
    h_w = D * (2.**(-0.4 * x**2)
               * (1. - 0.5 * 2.**(-0.003 * np.abs(-y - dc)**4)) - 0.9) / 0.9

    # Eastern shelf
    h_e = D * (2.**(-0.4 * (x - nx*rx)**2)
                * (1. - 0.5 * 2**(-0.003 * np.abs(-y - dc)**4)) - 0.9) / 0.9

    h = np.maximum(np.minimum(0., h_w), np.minimum(0., h_e))
    
    # Southern shelf
    h_s = -D*np.ones(h.shape)
    
    # Define masks
    m1 = y < -y_end + sws
    m2 = np.logical_and(-y_end + sws <= y, y < -y_end + 2*sws)
    m3 = np.logical_and(-y_end + 2*sws <= y, y < -y_end + 3*sws)
    
    h_s1 = -shelf_depth * (1. + ((y[m1] - (-y_end + sws))/sws)**3)
    h_s[m1] = h_s1
    
    h_s2 = -shelf_depth - (0.5 * (D - shelf_depth)
                           * ((y[m2] - (-y_end + sws))/sws)**3)
    h_s[m2] = h_s2
    
    h_s3 = -D - (0.5 * (D - shelf_depth)
                 * ((y[m3] - (-y_end + 3*sws))/sws)**3)
    h_s[m3] = h_s3

    h = np.maximum(h, h_s)

    # Flip sign for MOM
    h = -h
    h[h == 0.] = 0.

    return h


def save(depth, topog_fname=None):
    
    # Parse input arguments
    history = ' '.join(sys.argv)
    
    if not topog_fname:
        topog_fname = 'topog.nc'
    depth_name = 'depth'
    
    # Create output file
    topog_nc = nc.Dataset(topog_fname, 'w')
    
    # Global attributes
    topog_nc.grid_version = grid_version
    topog_nc.code_version = code_version
    topog_nc.history = history
    
    # Testing
    ntiles = 1
    ny, nx = depth.shape

    topog_nc.createDimension('ntiles', ntiles)
    topog_nc.createDimension('nx', nx)
    topog_nc.createDimension('ny', ny)
    
    depth_nc = topog_nc.createVariable(depth_name, 'f8', ('ny', 'nx'))
    depth_nc[:] = depth
    depth_nc.standard_name = 'topographic depth at T-cell centers'
    depth_nc.units = 'meters'
    
    topog_nc.close()


#---
if __name__ == '__main__':
    main()
