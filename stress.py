#!/usr/bin/env python
# coding: utf-8

import netCDF4 as nc
import numpy as np
import sys

#---
def save(tau_x, grid):
    # TODO: Promote tau to 2D vector
    
    history = ' '.join(sys.argv)
    
    # Default parameters
    stress_name = 'stress.nc'
    tau_x_name = 'taux'
    tau_y_name = 'tauy'
    
    # Testing
    grid_name = 'horizontal_grid.nc'
    grid_nc = nc.Dataset(grid_name, 'r')
    x_grid = grid_nc.variables['x'][1::2, 1::2]
    y_grid = grid_nc.variables['y'][1::2, 1::2]
    
    x = grid.x[0, :]
    y = grix.y[:, 0]
    t = np.zeros(1)
    
    nx = x.size
    ny = y.size
    nt = t.size
    
    # Create output file
    stress_nc = nc.Dataset(stress_name, 'w')
    
    stress_nc.createDimension('x', nx)
    stress_nc.createDimension('y', ny)
    stress_nc.createDimension('time', None)
    
    x_nc = stress_nc.createVariable('x', 'f8', ('x',))
    x_nc[:] = x
    
    y_nc = stress_nc.createVariable('y', 'f8', ('y',))
    y_nc[:] = y
    
    time_nc = stress_nc.createVariable('time', 'f8', ('time',))
    time_nc[:] = t
    time_nc.calendar = 'no_leap'
    time_nc.units = 'seconds since 0001-01-01 00:00:00'
    
    taux_nc = stress_nc.createVariable('taux', 'f8', ('time', 'y', 'x'))
    taux_nc[:] = tau_x
    
    stress_nc.close()
