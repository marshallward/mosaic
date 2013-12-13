#!/usr/bin/env python
# coding: utf-8

"""
Mercator grid generation
========================

Mercator grids are generated under the assumption of dx = dy,

.. math::
    \cos \phi d \lambda = d \phi

The integral of this relation is

\lambda(\phi) = \tan \left( \frac{\phi}{2} + \frac{\pi}{4} \right)

This mapping, and its inverse, are implemented in the `mercator_axis` and
`latitude_axis` functions, respectively.

To generate the grid:

    - Define a uniform longitude axis (lambda) over all latitudes
    - Map lambda to phi for each latitude

Features of Mercator grids (in contrast to spherical grids):
    -

"""

import numpy as np

r_Earth = 6.371009e6

def mercator_axis(lat):
    return np.log(np.tan(lat/2. + np.pi/4.))


def latitude_axis(y):
    return 2.*np.arctan(np.exp(y)) - np.pi/2.


def grid(lon_min, lon_max, lat_min, lat_max, d_lon_eq, dense_grid=True):

    # Double grid points for B-grid
    if dense_grid:
        d_lon = 0.5*d_lon_eq
    else:
        d_lon = d_lon_eq

    y_min = mercator_axis(np.deg2rad(lat_min))
    y_max = mercator_axis(np.deg2rad(lat_max))
    d_y = np.deg2rad(d_lon)

    # Adjust y_min and y_max as multiples of d_y
    # (so that the equator lies on the grid)
    y_min = np.round(y_min/d_y)*d_y
    y_max = np.round(y_max/d_y)*d_y

    N_y = int(1 + np.round((y_max - y_min)/d_y))
    y = np.linspace(y_min, y_max, N_y)
    lat_axis = latitude_axis(y)

    # Longitude axis
    N_lon = int(1 + np.round((lon_max - lon_min)/d_lon))
    lon_axis = np.deg2rad(np.linspace(lon_min, lon_max, N_lon))

    # Create the grids
    lon, lat = np.meshgrid(lon_axis, lat_axis)
    x = r_Earth * np.cos(lat) * lon
    y = r_Earth * lat

    g = Grid()

    g.nxp = N_lon
    g.nyp = N_y
    g.nx = N_lon - 1
    g.ny = N_y - 1

    g.x = np.rad2deg(lon)
    g.y = np.rad2deg(lat)
    g.dx = x[:,1:] - x[:,:-1]
    g.dy = y[1:,:] - y[:-1,:]
    g.area = (lon[:-1,1:] - lon[:-1,:-1]) \
                * (np.sin(lat[1:,:-1]) - np.sin(lat[:-1,:-1])) * r_Earth**2
    g.angle_dx = np.zeros([g.nyp, g.nxp])

    return g


class Grid():
    pass
