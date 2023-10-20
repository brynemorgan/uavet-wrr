#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2023'

__license__ = 'MIT'
__date__ = 'Fri 20 Oct 23 14:37:04'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           utils.py
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

#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import os
import pandas as pd
import pytz
import timezonefinder as tzf


out_fold = os.path.join( os.path.dirname( __file__ ), os.path.pardir, 'data')
tz = pytz.timezone(tzf.TimezoneFinder().timezone_at(lng=-120.,lat=34.))

def read_results(file, out_fold=out_fold, tz=tz, dt_cols=['Flight','FlightDateTime']):
    
    df = pd.read_csv(os.path.join(out_fold, file), parse_dates=[0])

    for dt_col in dt_cols:
        df[dt_col] = pd.to_datetime(df[dt_col], utc=True).dt.tz_convert(tz=tz)

    return df