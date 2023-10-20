#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'brynmorgan@ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2023'

__license__ = 'GNU General Public License v3.0'
__date__ = 'Wed 25 Jan 23 13:27:31'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           figs_ramajal.py
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
import pytz
import timezonefinder as tzf

from scipy import stats


import matplotlib.pyplot as plt
import matplotlib as mpl

import seaborn as sns

# Temporary patch to use code from ecflux until packaged + released...
if not any('aeroet' in x for x in sys.path):
    sys.path.append('/Users/brynmorgan/dev/aeroet/src/')

# aeroet
from aeroet import AirLayer #, Surface, Radiation
from aeroet.uncertainty import utils as sens


import utils
import utils_figs as figs
# import utils_sensitivity as sens


#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------
out_fold = os.path.join( os.path.dirname( __file__ ), os.path.pardir, 'data')
# '/Users/brynmorgan/Library/Mobile Documents/com~apple~CloudDocs/Dangermond/Figures/23W/'
tz = pytz.timezone(tzf.TimezoneFinder().timezone_at(lng=-120.,lat=34.))

def plot_met_variable(ax, x, y, var_name, lims=None, offset=0.1, labels=[r"$z_1$", r"$z_2$"], err_stats=False, colors=['C0','C1'], **kwargs):

    if not lims:
        try:
            lims = figs.get_lims([x, *y], offset=offset)
        except:
            lims = figs.get_lims([*x, *y], offset=offset)

    line = np.arange(lims[0], lims[1]+1, (lims[1]-lims[0])/10)

    # Plot one-to-one line
    ax.plot(line, line, color='k', linewidth=0.8)
    # Plot data
    rmses = []
    r2s = []
    resids = []

    for x_i,y_i,lab,c in zip(x, y, labels, colors):
        # ax.plot(x_i, y_i, '.', alpha=0.6, label=lab, markeredgecolor='none', **kwargs)
        ax.scatter(x_i, y_i, label=lab, edgecolor='none', s=20, c=c, **kwargs)

        # mask = x_i == y_i
        # mask = [True if flight.met_data is not None else False for flight in flights]
        mask = (abs(x_i - y_i) < 1e-4) | (x_i < 0)

        if err_stats:
            r2 = np.round(figs.calc_r2(y_i[~mask], x_i[~mask]), 2)
            rmse = np.round(figs.calc_rmse(y_i[~mask], x_i[~mask]), 2)

            rmses.append(rmse)
            r2s.append(r2)
            resids.append(figs.calc_mbe(y_i[~mask], x_i[~mask]))

    ax.set_xlim(*lims)
    ax.set_ylim(*lims)

    if err_stats:    
        n = 0
        for j,(rmse,r2) in enumerate(zip(rmses,r2s)):
            ax.annotate(
                r"RMSD = {rmse:.2f}, $r^2$ = {r2:.2f}".format(rmse=rmse, r2=r2),
                (0.03,0.925+n), xycoords='axes fraction', color = colors[j][0]
            )
            n += -0.075
    # ax.set_xlabel('Tower ' + var_name)
    # ax.set_ylabel('UAV ' + var_name)
    # ax.legend()
    return rmses,r2s,resids



#-------------------------------------------------------------------------------
# READ IN DATA
#-------------------------------------------------------------------------------

# Import calculated UAV fluxes
uav_flux = utils.read_results('ramajal_models.csv')
uav_flux.set_index('FlightDateTime',inplace=True, drop=False)
# Import met data for UAV flights with thermal data
uav_met = utils.read_results('ramajal_met.csv')
uav_met.set_index('FlightDateTime',inplace=True, drop=False)
# Import met data for all UAV flights
uav_met_all = utils.read_results('ramajal_all_met.csv')
uav_met_all.set_index('FlightDateTime',inplace=True, drop=False)
# Copy met data for UAV flights without thermal data to new dataframe
uav_met_flir = uav_met_all.drop(index=uav_met.index)

# Read tower data for all flights
tower_ram = utils.read_results('tower_all.csv', dt_cols=['FlightDateTime','date_time'])
tower_ram.set_index('FlightDateTime',inplace=True, drop=True)
# Copy tower data for flux flights
tower = tower_ram.loc[uav_met.index].copy()

# Read footprint results
fp_df = utils.read_results("ramajal_fp_stats.csv", dt_cols=['Flight', 'FlightDateTime'])

#-------------------------------------------------------------------------------
# COLORS + PLOT SETTINGS
#-------------------------------------------------------------------------------
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = 'Myriad Pro'
# mpl.rcParams['font.sans-serif'] = 'Source Sans Pro'
mpl.rcParams['font.size'] = 12.0
mpl.rcParams['axes.titlesize'] = 12.0

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

y_names = [r"$T_{a,\mathrm{UAV}}$ (°C)", r"$h_{r, \mathrm{UAV}}$ (%)", r"$p_{a, \mathrm{UAV}}$ (kPa)", r"$u_{, \mathrm{UAV}}$ (m s$^{-1}$)"]
x_names = [r"$T_{a,\mathrm{EC}}$ (°C)", r"$h_{r, \mathrm{EC}}$ (%)", r"$p_{a, \mathrm{EC}}$ (kPa)", r"$u_{, \mathrm{EC}}$ (m s$^{-1}$)"]

met_colors = ['#9E8510', figs.c_pa1]
rad_colors = [figs.c_Ta1, figs.c_Ta, figs.c_hr1, '#60A8AC', figs.c_rH]
mod_colors = [figs.c_Ts, figs.c_pa1, '#60a8ac', figs.c_Ta]


#-------------------------------------------------------------------------------
# FIG. 3. TOWER PROFILES VS. UAV MET
#-------------------------------------------------------------------------------

met_vars = ['T_a', 'h_r', 'p_a', 'u']
tower_vars = ['T_a', 'h_r', 'p_a', 'u']

uav_df = uav_met_all
tow_df = tow_ram

# Set alpha values for non-flux flights for plotting
alph = pd.Series([0.9]*len(uav_df), index=uav_df.index)
alph.loc[uav_met.index] = 1.0

# Colors
m_colors = pd.DataFrame(
    {'c1' : ['#d7cd9d']*len(uav_df), 'c2' : ['#99BABA']*len(uav_df)},
    index=uav_df.index
) 
m_colors.c1.loc[uav_met.index] = met_colors[0] #figs.c_Ta1
m_colors.c2.loc[uav_met.index] = met_colors[1] #figs.c_hr2

# Create tower profiles
tow_atmos = sens.create_atmosphere(tow_df, d_0=0.195, le_col='LE')
tow_air1 = sens.create_air_z(1.5, tow_atmos)
tow_air2 = sens.create_air_z(uav_df.z_2, tow_atmos)

tow_air_df = pd.DataFrame({
    # 'Flight' : uav_met.Flight,
    'T_a_1' : tow_air1.T_a, 'T_a_2' : tow_air2.T_a,
    'h_r_1' : tow_air1.h_r, 'h_r_2' : tow_air2.h_r,
    'p_a_1' : tow_air1.p_a, 'p_a_2' : tow_air2.p_a,
    'u_1' : tow_air1.u, 'u_2' : tow_air2.u,
    'theta_a_1' : tow_air1.theta_a, 'theta_a_2' : tow_air2.theta_a,
    'q_1' : tow_air1.q, 'q_2' : tow_air2.q,
})

# PLOT
#-------
abc_list = ['(a)','(b)','(c)','(d)']

met_resids = {}

fig = plt.figure(figsize=[9.4,8])
# fig = plt.figure(figsize=[7.4,6.3])

for i,(var,x_lab,y_lab,abc) in enumerate(zip(met_vars, x_names, y_names, abc_list)):

    ax = fig.add_subplot(2,2,i+1)

    if var == 'T_a':
        x = tow_air_df[var + '_1'] - 273.15, tow_air_df[var + '_2'] - 273.15
        y = [uav_df[var + '_1']-273.15, uav_df[var + '_2']-273.15]
    else:
        x = tow_air_df[var + '_1'], tow_air_df[var + '_2'] 
        y = [uav_df[var + '_1'], uav_df[var + '_2']]

    rmses,r2s,resids = plot_met_variable(ax, x, y, var, err_stats=True, alpha=alph, colors=[m_colors.c1.to_list(),m_colors.c2.to_list()]) #, markersize=12)
    
    met_resids[var] = resids
    met_resids[var+'_MAE'] = [figs.calc_mae(y[0],x[0]), figs.calc_mae(y[1],x[1])]

    ax.set_xlabel(x_lab)
    ax.set_ylabel(y_lab)
    ax.annotate(abc, xy=(0.01,1.03), xycoords='axes fraction')

    if i == 1:
        ax.legend(bbox_to_anchor=(1.04, 1.01), loc="upper left")

plt.tight_layout()

# plt.savefig(os.path.join(fig_fold, 'met.eps'), dpi=600)
# plt.savefig(os.path.join(fig_fold, 'met.pdf'), dpi=600)
# plt.savefig(os.path.join(fig_fold, 'met.png'), dpi=600)


# plt.savefig(os.path.join(fig_fold, 'met_trans.eps'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'met_trans.pdf'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'met_trans.png'), dpi=600, transparent=True)

#-------------------------------------------------------------------------------
# FIG. 4. TOWER VS. UAV RADIATION
#-------------------------------------------------------------------------------
rad_markers = ['v','^','v', '^', 'o']

mpl.rcParams['font.size'] = 11.0

rad_resids = {}

fig = plt.figure(figsize=[5.8,5])


lims = [0, 850.]
line = np.arange(lims[0], lims[1]+1, (lims[1]-lims[0])/10)
plt.plot(line, line, color='k', linewidth=0.8)


for i,var in enumerate(['SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'R_n']):
    x = tower[var]
    if var + '_fp' in uav_met.columns:
        y = uav_met[var]
    elif i > 0:
        y = uav_met[var + '_mean']
    else:
        y = uav_met[var]
    # if i == 1:

    mask = x != y
    x = x[mask]
    y = y[mask]

    r2 = np.round(figs.calc_r2(y, x), 2)
    rmse = np.round(figs.calc_rmse(y, x), 2)
    rad_resids[var] = (figs.calc_mbe(y, x))
    rad_resids[var+'_MAE'] = (figs.calc_mae(y,x))

    label = figs.var_dict.get(var)['symbol'] + r"(RMSD = {rmse}, $r^2$ = {r2})".format(rmse=rmse,r2=r2)

    plt.scatter(x, y, c=rad_colors[i], linewidth=0.0, alpha=0.85, label=label, marker=rad_markers[i])

plt.xlabel(r"Tower radiation (W m$^{-2}$)")
plt.ylabel(r"UAV radiation (W m$^{-2}$)")

plt.xlim(lims)
plt.ylim(lims)

plt.legend(loc='upper left')

plt.tight_layout()

mpl.rcParams['font.size'] = 12.0

# plt.savefig(os.path.join(fig_fold, 'rad.eps'), dpi=600)
# plt.savefig(os.path.join(fig_fold, 'rad.pdf'), dpi=600)
# plt.savefig(os.path.join(fig_fold, 'rad.png'), dpi=600)

# plt.savefig(os.path.join(fig_fold, 'rad_trans.eps'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'rad_trans.pdf'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'rad_trans.png'), dpi=600, transparent=True)

#-------------------------------------------------------------------------------
# FIG. 5. TOWER VS. UAV FLUXES
#-------------------------------------------------------------------------------

mpl.rcParams['font.size'] = 14.0

uav_swm = uav_flux.pivot(columns=['Variable','Model'], values='SRC_WT_MEAN')

a,b,r,p,se = stats.linregress(tower.LW_OUT, tower.G)

resids = {}

fig = plt.figure(figsize=(12.0,5.0))

for i,var in enumerate(['H', 'LE']):
    ax = fig.add_subplot(1,2,i+1)

    if var == 'LE':
        x = tower.LE_corr_LE 
        # x = ep.LE
        # an_x = 0.55
        an_x = 0.52
        an_y = 0.22 #0.05
        an_n = -0.055
    else:
        x = tower[var] 
        # x = ep.H
        an_x = 0.03
        an_y = 0.94
        an_n = -0.055

    lims = figs.get_lims([x, *[uav_swm[var][col] for col in uav_swm[var].columns]], offset=0.1)
    line = np.arange(lims[0], lims[1]+1, (lims[1]-lims[0])/10)
    ax.plot(line, line, color='k', linewidth=0.8)
    ax.set_xlim(*lims)
    ax.set_ylim(*lims)

    rmses = []
    r2s = []
    mapes = []

    for method,c in zip(list(utils.mod_dict.keys()),mod_colors):
        y = uav_swm[var][method]

        rmse = figs.calc_rmse(y, x)
        r2 = figs.calc_r2(y, x)
        mape = figs.calc_mape(y, x)

        rmses.append(rmse)
        r2s.append(r2)
        mapes.append(mape)
        resids[var + '_' + method] = y-x
        
        label = method # + r" (RMSE = {rmse:.3f}, $MAPE$ = {mape:.3f})".format(rmse=rmse, mape=mape) 
        

        sns.regplot(
            x=x, y=y, color=c, scatter=True, label=label, truncate=True,
            scatter_kws={'linewidth' : 0, 's' : 40}, line_kws={'linewidth' : 1.8}
        )

    ax.set_xlabel(figs.var_dict.get(var)['symbol'] + r"$_{\mathrm{EC}}$ (W m$^{-2}$)")
    ax.set_ylabel(figs.var_dict.get(var)['symbol'] + r"$_{\mathrm{UAV}}$ (W m$^{-2}$)")

    # Add RMSD and r2 values to plot
    n = 0
    for j,(rmse,r2) in enumerate(zip(rmses,r2s)):
        ax.annotate(
            r"RMSD = {rmse:.2f}, $r^2$ = {r2:.2f}".format(rmse=rmse, r2=r2),
            (an_x,an_y+n), xycoords='axes fraction', color = mod_colors[j]
        )
        n += an_n

    ax.annotate(abc_list[i], xy=(0.01,1.03), xycoords='axes fraction')

    # Add legend
    if var == 'LE':
        # ax.set_yticklabels([])
        ax.legend(bbox_to_anchor=(1.0, 1), loc="upper left", handletextpad=0.5)

mpl.rcParams['font.size'] = 12.0

plt.tight_layout()

# plt.savefig(os.path.join(fig_fold, 'flux_rev_fp.eps'), dpi=600)
# plt.savefig(os.path.join(fig_fold, 'flux_rev_fp.pdf'), dpi=600)
# plt.savefig(os.path.join(fig_fold, 'flux_rev_fp.png'), dpi=600)

# plt.savefig(os.path.join(fig_fold, 'flux_rev_fp_trans.eps'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'flux_rev_fp_trans.pdf'), dpi=600, transparent=True)
# plt.savefig(os.path.join(fig_fold, 'flux_rev_fp_trans.png'), dpi=600, transparent=True)