#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'brynmorgan@ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2023'

__license__ = 'MIT'
__date__ = 'Thu 19 Oct 23 12:41:59'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           example.py
Compatibility:  Python 3.10.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       None

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        brynmorgan@ucsb.edu
Copyright:      (c) Bryn Morgan 2023


"""

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------

import os
import sys
import numpy as np
import pandas as pd
import datetime
import pytz
# import shapely

import xarray as xr

import geopandas as gpd
import shapely


import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

%matplotlib qt

from xarray import DataArray

from ortho import MicaSenseOrtho
import utils


if not any('aeroet' in x for x in sys.path):
    sys.path.append('/Users/brynmorgan/dev/aeroet/src')
# aeroet
from aeroet import AirLayer, Surface, Radiation
from aeroet import radiation, model

import utils_figs as figs
#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
def set_crs(arr, crs):
    arr.rio.set_crs(crs)

#-------------------------------------------------------------------------------
# DATA IMPORT
#-------------------------------------------------------------------------------

uav_met = utils.read_results('ramajal_met.csv')
uav_met.set_index('FlightDateTime',inplace=True, drop=False)

# Import ortho
# config
ortho_config = {
    'dt_format': '%Y%m%d_%H%M%S',
    'skip_char': '0',
    'end_char': '0',
}

# Read ortho
ortho = MicaSenseOrtho(file='../data/Ramajal_20210324_115832.tif', config=ortho_config)
ortho.init()
# Get LST and NDVI
T_s = ortho.get_temperature()
ndvi = ortho.calc_ndvi()

#-------------------------------------------------------------------------------
# CREATE MODEL PARAMETERS
#-------------------------------------------------------------------------------

# Site parameters
h = 0.3
w_l = 0.01
theta_sun = 35.72088909219039
x_lad = 0.

air_vars = ['z','u','T_a','h_r','p_a']

# Get SW incoming radiation
SW_IN = uav_met.SW_IN[1]

# Create airlayers
air1 = AirLayer(**dict(zip(air_vars, uav_met[[var+'_1' for var in air_vars]].iloc[1].values)), z_0=h)
air2 = AirLayer(**dict(zip(air_vars, uav_met[[var+'_2' for var in air_vars]].iloc[1].values)), z_0=h)


# Create a surface
surf = Surface(
    h=h, T_s=T_s, w_l=w_l, ndvi=ndvi, x_lad=x_lad, theta_sun=theta_sun,
)
surf.T_s = surf.correct_T_b(
    LW_IN = radiation.calc_LW(air2.T_a, air2.calc_emissivity()),
    T_a = air2.T_a,
    # tau = temp.calc_tau(wvc = air2.calc_wvc(), d = air2.z - surf.h),
    tau = air2.calc_tau(wvc = air2.calc_wvc(), d = air2.z - surf.h),
    epsilon_s = surf.epsilon_s
)

# Create radiation object
# 1. Albedo
alpha = surf.albedo
# 2. SW OUTGOING
SW_OUT = radiation.calc_SW_out(SW_IN, alpha)    

# 3. LW INCOMING
LW_IN = radiation.calc_LW(air1.T_a, air1.calc_emissivity()) * surf.epsilon_s
# 4. LW OUTGOING
LW_OUT = radiation.calc_LW(surf.T_s, surf.epsilon_s)
set_crs(LW_IN, surf.T_s.rio.crs)
set_crs(LW_OUT, surf.T_s.rio.crs)

# Soil heat flux parameters
G_params = {
    'A' : 0.17860959, 
    'c' : -4.14198702,
    't' : 12.123472222222222,
}

rad = Radiation(SW_IN, SW_OUT, LW_IN, LW_OUT, G=None, G_params=G_params)
set_crs(rad.R_n, surf.T_s.rio.crs)
rad.set_components(SW_IN, SW_OUT, LW_IN, LW_OUT)


#-------------------------------------------------------------------------------
# RUN MODEL
#-------------------------------------------------------------------------------

mod = model.BrutsaertModel(airlayer=air2, surface=surf, radiation=rad)
mod.run(allow_neg_flux=False)


#-------------------------------------------------------------------------------
# PLOT (FIG. 5)
#-------------------------------------------------------------------------------


def plot_raster(
    raster, ax, cmap=None, crange=None, cb_ticks=None, cb_ticklabels=None, units=None, 
    point=None, point_kwargs=None
):

    im = ax.imshow(raster, cmap=cmap)
    # if point:
    #     ax.scatter(*point, **point_kwargs)
    ax.set_axis_off()

    cb = fig.colorbar(im, ax=ax, orientation='horizontal', shrink=0.6)
    if crange:
        im.set_clim(crange[0],crange[1])
    if cb_ticks:
        cb.set_ticks(cb_ticks)
        if cb_ticklabels:
            cb.set_ticklabels(cb_ticklabels)
        elif units:
            cb.set_ticklabels([str(t) + ' ' + units for t in cb_ticks])
    cb.outline.set_linewidth(0) 

    return ax,cb

def get_tower_point(ortho, tower_coords=(737168.6913608506, 3823582.6557895136)):
    x_min = ortho.x.min().item()
    y_min = ortho.y.min().item()
    y_max = ortho.y.max().item()
    x_utm,y_utm = tower_coords

    res = ortho.rio.resolution()[0]

    x = (x_utm-x_min)/res
    y = (y_max-y_utm)/res

    return (x,y)



ndvi = mod.surface.ndvi
T_s = mod.surface.T_s-273.15
LE = mod.LE.copy()

mask = xr.where(mod.radiation.R_n.notnull(), x=0., y=np.nan)

LE = LE.where(LE.notnull(), mask)

x_tow,y_tow = get_tower_point(ortho.ortho_array)

abc_list = ['(a)', '(b)', '(c)', '(d)']

rasters = [ndvi, T_s, LE]
labs = ['NDVI', r"$T_s$", r"$\lambda E$"]

c_kwargs = [
    {
        'crange' : [0.0,1.0],
        'cb_ticks' : [0.0,0.2,0.4,0.6,0.8,1.0],
        'cb_ticklabels' : None
    },
    {
        'crange' : [20.,40.],
        'cb_ticks' : list(np.arange(20.,41.,5.)),
        'cb_ticklabels' : [20, 25, 30, 35, r"40°C"]
    },
    {
        'crange' : [0.0,600.],
        'cb_ticks' : list(np.arange(0.,601.,200.)),
        'cb_ticklabels' : [0, 200, 400, r"600 W m$^{-2}$"]
    }
]


ndvi_map = figs.get_continuous_cmap(
 ['8a6f24', 'ab8622', 'cc9d20', 'dfcb68', 'f2f8af', 
  'badf6e', '81c52c', '61a923', '418d1a', '2f5226']
)

temp_colors = [
    "00494e","006e7a","32a8ae","68c4c3","9ee0d8",
    "d2fcd5","f2f8af","f6e551","fab42f","#F9614D"
]
temp_map = figs.get_continuous_cmap(temp_colors)
le_colors = ["e9feea","d2fcd5","9ee0d8","64c6c0","32a8ae","006e7a"]
le_map = figs.get_continuous_cmap(le_colors)



maps = [ndvi_map, temp_map, le_map]

fig, axs = plt.subplots(1, 3, figsize=(10., 4.5), sharey=True, layout='constrained')

for i,(raster,ax) in enumerate(zip(rasters,axs.flat)):

    ax,cb = plot_raster(
        raster, ax=ax, **c_kwargs[i],cmap=maps[i], 
        #point=ramajal.get_utm_coords(), point_kwargs= {'marker': '.', 'c':'k', 's' : 20}
    )
    # ax.annotate('.', xy=ramajal.get_utm_coords(), xycoords='data')
    ax.scatter(x_tow, y_tow, s=25, c='k', marker='^')
    cb.set_label(labs[i])
    ax.annotate(abc_list[i], xy=(0.01,1.0), xycoords='axes fraction')

dx = 18/72.; dy = 10/72. 
offset = mpl.transforms.ScaledTranslation(dx, 0/72., fig.dpi_scale_trans)

label = cb.ax.xaxis.get_majorticklabels()[-1]
label.set_transform(label.get_transform() + offset)


scalebar = AnchoredSizeBar(
    ax.transData,
    2040.5498057397074, '50 m', 'upper right', 
    pad=0.0,
    borderpad=0.0,
    color='k',
    frameon=False,
    size_vertical=1,
    # bbox_to_anchor=(0.973,0.205), # png
    bbox_to_anchor=(0.953,0.205), # pdf
    # bbox_to_anchor=mpl.transforms.Bbox.from_bounds(0, 0, 1, 1),
    bbox_transform=ax.figure.transFigure,
    # fontproperties=fontprops
)

ax.add_artist(scalebar)


# plt.savefig(os.path.join(fig_fold, 'orthos_rev.eps'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'orthos_rev.pdf'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'orthos_rev.png'), dpi=600, transparent=True)


