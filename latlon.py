#!/usr/bin/env python
# coding: utf-8

import numpy as np

r_Earth = 6.371009e6

def grid(lon_min, lon_max, lat_min, lat_max, d_lon,
         d_lat=None, dense_grid=True):

    if not d_lat:
        d_lat = d_lon

    # Double grid points for B-grid
    if dense_grid:
        d_lon = 0.5 * d_lon
        d_lat = 0.5 * d_lat

    N_lat = int(1 + np.round((lat_max - lat_min)/d_lat))
    lat_axis = np.deg2rad(np.linspace(lat_min, lat_max, N_lat))

    N_lon = int(1 + np.round((lon_max - lon_min)/d_lon))
    lon_axis = np.deg2rad(np.linspace(lon_min, lon_max, N_lon))

    # Create the grids
    lon, lat = np.meshgrid(lon_axis, lat_axis)
    x = r_Earth * np.cos(lat) * lon
    y = r_Earth * lat

    g = Grid()

    g.nxp = N_lon
    g.nyp = N_lat
    g.nx = N_lon - 1
    g.ny = N_lat - 1

    g.x = np.rad2deg(lon)
    g.y = np.rad2deg(lat)
    g.dx = x[:, 1:] - x[:, :-1]
    g.dy = y[1:, :] - y[:-1, :]
    g.area = (lon[:-1, 1:] - lon[:-1, :-1]) \
                * (np.sin(lat[1:, :-1]) - np.sin(lat[:-1, :-1])) * r_Earth**2
    g.angle_dx = np.zeros([g.nyp, g.nxp])

    return g


class Grid():
    pass
