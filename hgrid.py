#!/usr/bin/env python
# coding: utf-8

import netCDF4 as nc
import numpy as np
import sys

from mosaic import mercator as merc

# Parameters
string_len = 255
grid_version = '0.2'
tagname = '$Name: siena_201203 $'

"""
Reproduction of make_hgrid.c
Contact:    Marshall Ward (marshall.ward@anu.edu.au)
"""

make_hgrid_desc = """
Description of make_hgrid here.
"""

def save(grid, grid_name=None):
    
    # Parse input arguments
    history = ' '.join(sys.argv)
    
    # Default parameters
    # TODO: Derive parameters from grid
    if not grid_name:
        grid_name = 'horizontal_grid.nc'
    center = None
    geometry = 'spherical'
    projection = None
    arcx = 'small_circle'
    north_pole_tile = '0.0 90.0'
    discretization = 'logically_rectangular'
    conformal = 'true'
    north_pole_arcx = 'small_circle'
    
    # TODO: Mosaic tile implementation
    tile_name = 'tile1'
    
    # Create output file
    grid_nc = nc.Dataset(grid_name, 'w')
    
    # Global attributes
    grid_nc.grid_version = grid_version
    grid_nc.code_version = tagname
    grid_nc.history = history
    
    grid_nc.createDimension('string', string_len)
    grid_nc.createDimension('nx', grid.nx)
    grid_nc.createDimension('ny', grid.ny)
    grid_nc.createDimension('nxp', grid.nxp)
    grid_nc.createDimension('nyp', grid.nyp)
    
    # Mosaic tile properties
    tile_nc = grid_nc.createVariable('tile', 'S1', ('string',))
    tile_nc[:len(tile_name)] = list(tile_name)
    tile_nc.standard_name = 'grid_tile_spec'
    tile_nc.geometry = geometry
    if north_pole_tile:
        tile_nc.north_pole_tile = north_pole_tile
        if projection:
            tile_nc.projection = projection
    tile_nc.discretization = discretization
    tile_nc.conformal = conformal
    
    # Grid variables
    x_nc = grid_nc.createVariable('x', 'f8', ('nyp', 'nxp'))
    x_nc[:] = grid.x
    x_nc.standard_name = 'geographic_longitude'
    x_nc.units = 'degree_east'
    
    y_nc = grid_nc.createVariable('y', 'f8', ('nyp', 'nxp'))
    y_nc[:] = grid.y
    y_nc.standard_name = 'geographic_latitude'
    y_nc.units = 'degree_north'
    
    dx_nc = grid_nc.createVariable('dx', 'f8', ('nyp', 'nx'))
    dx_nc[:] = grid.dx
    dx_nc.standard_name = 'grid_edge_x_distance'
    dx_nc.units = 'meters'
    
    dy_nc = grid_nc.createVariable('dy', 'f8', ('ny', 'nxp'))
    dy_nc[:] = grid.dy
    dy_nc.standard_name = 'grid_edge_y_distance'
    dy_nc.units = 'meters'
    
    area_nc = grid_nc.createVariable('area', 'f8', ('ny', 'nx'))
    area_nc[:] = grid.area
    area_nc.standard_name = 'grid_cell_area'
    area_nc.units = 'm2'
    
    angle_dx_nc = grid_nc.createVariable('angle_dx', 'f8', ('nyp', 'nxp'))
    angle_dx_nc[:] = grid.angle_dx
    angle_dx_nc.standard_name = 'grid_vertex_x_angle_WRT_geographic_east'
    angle_dx_nc.units = 'degrees_east'
    
    if not conformal:
        angle_dy_nc = grid_nc.createVariable('angle_dy', 'f8', ('nyp', 'nxp'))
        angle_dy_nc[:] = grid.angle_dy
        angle_dy_nc.standard_name = 'grid_vertex_y_angle_WRT_geographic_north'
        angle_dy_nc.units = 'degrees_north'
    
    arcx_nc = grid_nc.createVariable('arcx', 'S1', ('string',))
    arcx_nc[:len(arcx)] = list(arcx)
    arcx_nc.standard_name = 'grid_edge_x_arc_type'
    if north_pole_arcx:
        arcx_nc.north_pole = north_pole_arcx
    
    grid_nc.close()


class Grid(object):
    pass
