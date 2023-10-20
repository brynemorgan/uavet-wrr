#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2023'

__license__ = 'MIT'
__date__ = 'Tue 09 May 23 17:00:52'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           correct_temp.py
Compatibility:  Python 3.7.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       None

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        bryn.morgan@geog.ucsb.edu
Copyright:      (c) Bryn Morgan 2023


"""


# IMPORTS
import os
import numpy as np

# FUNCTIONS

lin_dictK = {
    'ALL': {
        'Slope': 1.3372275455889693,
        'Intercept': -100.3186114647923,
        'R2': 0.9729385601878838,
        'p': 4.659623104386496e-77,
        'StandardError': 0.022761581779130145,
        'n': 98.0
    },
    'SN52': {
        'Slope': 1.3833264937415755,
        'Intercept': -113.98306486902885,
        'R2': 0.989836426080431,
        'p': 1.7321813592697283e-87,
        'StandardError': 0.015115307204487503,
        'n': 88.0
    },
    'SN75': {
        'Slope': 2.0420170197772127,
        'Intercept': -302.5531588952041,
        'R2': 0.9797085443176952,
        'p': 4.673762542514119e-08,
        'StandardError': 0.10390166764074067,
        'n': 10.0
    },
    'TSM835' : {
        'Slope': 1.45827975603128,
        'Intercept': -133.7750913120778,
        'R2': 0.8782068231891249,
        'p': 6.334147950807622e-05,
        'StandardError': 0.19200340440110228,
        'n': 10
    },
    'TSM836' : {
        'Slope': 1.6342506432252804,
        'Intercept': -184.40744294056253,
        'R2': 0.9495500801411989,
        'p': 1.8082468902806203e-06,
        'StandardError': 0.1331818287626371,
        'n': 10
    },
}

lin_dictC = {
    'ALL': {
        'Slope': 1.3372275455889686,
        'Intercept': -8.204907387165282,
        'R2': 0.9729385601878832,
        'p': 4.6596231043920595e-77,
        'StandardError': 0.022761581779130423,
        'n': 98.0
    },
    'SN52': {
        'Slope': 1.3833264937415755,
        'Intercept': -9.277433103517499,
        'R2': 0.9898364260804314,
        'p': 1.7321813592664788e-87,
        'StandardError': 0.015115307204487172,
        'n': 88.0
    },
    'SN75': {
        'Slope': 2.0420170197772127,
        'Intercept': -17.926209943058637,
        'R2': 0.9797085443176954,
        'p': 4.6737625425139105e-08,
        'StandardError': 0.10390166764074009,
        'n': 10.0
    }
}

def f(x, a, b):
    y = a * x + b
    return y

def get_met_sn(flight):
    if flight.met_data:
        try:
            sn = os.path.basename(flight.met_data.filename)[6:10]
        except:
            sn = os.path.basename(flight.met_data.filename[0])[6:10]
    else:
        sn = np.nan
    
    return sn

# os.path.join( os.path.dirname( __file__ ), os.path.pardir, os.path.pardir, 'data')


def correct_Ta(T, lin_dict=lin_dictK, sn='ALL'):

    ld = lin_dict.get(sn, 'ALL')

    T_corr = f(T, ld.get('Slope'), ld.get('Intercept'))

    return T_corr
