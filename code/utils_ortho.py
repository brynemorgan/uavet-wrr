#!usr/bin/env python
# -*- coding: utf-8 -*-
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'brynmorgan@ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2021'

__license__ = 'MIT'
__date__ = 'Fri 19 Feb 21 13:53:34'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           utils.py
Compatibility:  Python 3.10.0
Description:    Contains general functions for working with UAV data.

Requires:       os, re, datetime, pytz, timezonefinder, numpy, logging

Dev ToDo:       Partial copy from ecoflydro.utils. Not intended to be used separately.

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        brynmorgan@ucsb.edu
Copyright:      (c) Bryn Morgan 2021


"""


#-------------------------------------------------------------------------------
# IMPORTS
#-------------------------------------------------------------------------------
import os
import re

import datetime
import pytz
import timezonefinder as tzf

import numpy as np

import logging


# from .config import config

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------

flir_dict = {
    'RJPEG': {
        'dt_key': 'DateTimeOriginal',
        'dt_format': '%Y:%m:%d %H:%M:%S.%f%z',
        'end_char': 6,
    },
    'TIFF': {
        'dt_key': 'SubSecDateTimeOriginal',
        'dt_format': '%Y:%m:%d %H:%M:%S.%f',
        'end_char': 4,
    },
    'JPEG': {
        'dt_key': 'FileModifyDate',
        'dt_format': '%Y:%m:%d %H:%M:%S%z',     # Note: the time is local to the machine
        'end_char': 7,
    }
}


#-------------------------------------------------------------------------------

'''
Functions
---------
    filename_to_dt()
        Converts filename string to datetime format. Intended to be used for:
            'DJI'   –  UAV flight log file
            'DL222' –  DL222 .txt file with metdata
            'FLIR'  –  FLIR folder
            'IMG'   –  FLIR image (don't use; need to fix)
            'MICA'  –  MicaSense image/folder (not implemented)

    dms_to_dd()
        Converts coordinate value from degrees, minutes, seconds to decimal degrees.

    round_dt_to_ms()
        Rounds timestamp to nearest millisecond.

    make_tzaware()
        Converts naive datetime object to timezone-aware object based on timezone
        name, coordinates, or fixed UTC offset.

    get_env_data_as_dict()
        Reads environment variables from the provided file and returns
        a dictionary of key-value pairs.

'''


def get_env_data_as_dict(path: str) -> dict:
    with open(path, 'r') as f:
        return dict(tuple(line.replace('\n', '').split('=')) for line
                    in f.readlines() if not line.startswith('#'))



def extract_float(dirty_str):
    """
    Extracts the float value of a string (helpful for parsing the exiftool data).

    Parameters
    ----------
    dirty_str : str
        The string from which to parse the float

    Returns
    -------
    flt : float or list
        The value of the parsed string as a float or list of floats.

    Modified from https://github.com/nationaldronesau/FlirImageExtractor/blob/master/flir_image_extractor_cli/flir_image_extractor.py
    """

    try:
        float(dirty_str)
        return float(dirty_str)
    except:
        digits = re.findall(r"[-+]?\d*\.\d+|\d+", dirty_str)

        if len(digits) == 1:
            flt = float(digits[0])
        else:
            flt = [float(dig) for dig in digits]

        return flt




def filename_to_dt(file, skip_char=0, end_char=0, dt_format=None, **kwargs):
    '''
    Converts filename string to datetime format. Can be used for any file with
    datetime info in the filename by specifying skip_char, end_char, and dt_format.

    Parameters
    ----------
    file : str
        filename to be converted

    skip_char : int
        The number of characters at the beginning of the filename to skip when
        converting the timestamp. The default is 0. This should be 6 for DL222.

    end_char : int
        The number of characters at the end of the filename (excluding the
        extension) to skip when converting to timestamp. The default is 0. This
        should be 2 for radiometric JPGs from FLIR Duo Pro R.

    dt_format : str
        The format of the file names's datetime information. The default is None,
        so the format is defined by the source.

    **kwargs
        Optional keyword arguments to pass to make_tzaware().

    Returns
    -------
    dt : datetime object
        Filename as a datetime object.
    '''

    # Get basename of file without extension
    base = os.path.splitext(os.path.basename(file))[0]

    # Exclude all characters except timestamp
    dt_str = base[skip_char:len(base)-end_char]
    # Convert string to datetime
    dt = datetime.datetime.strptime(dt_str, dt_format)

    # Make tzaware
    dt = make_tzaware(dt, **kwargs)

    return dt


def dms_to_dd(dms):
    """
    Converts coordinate value from degrees, minutes, seconds to decimal degrees.

    Parameters
    ----------
    dms : list
        List of the form [deg, min, sec].

    Returns
    -------
    dd : float
        Coordinate in decimal degrees.
    """
    dd = dms[0] + float(dms[1])/60 + float(dms[2])/3600

    return dd


def round_dt_to_ms(dt):
    """
    Rounds timestamp to nearest millisecond.

    Parameters
    ----------
    dt : datetime object
        Datetime object to be converted.

    Returns
    -------
    dt_ms : datetime object
        Datetime object rounded to nearest millisecond.
    """
    tz = dt.tzinfo

    ts = np.round(dt.timestamp(), 1)

    dt_ms = datetime.datetime.fromtimestamp(ts, tz=tz)

    return dt_ms


def make_tzaware(dt_naive, tz_name='America/Los_Angeles', coords=None, utc_offset=None):
    """
    Converts naive datetime object to timezone-aware object based on one of the
    following:
        1. Timezone name (default)
        2. Geographic coordinates
        3. Fixed UTC offset

    Note: the timestamp provided is not *converted* to the given timezone; the
    timezone is simply attached. Thus the provided timezone info should be that
    of the naive datetime object.

    Parameters
    ----------
    dt_naive : datetime object
        Naive datetime object to be made aware.

    tz_name : str
        Name of timezone. Must be one of the valid timezones listed in pytz.alltimezones.
        The default is 'America/Los_Angeles'. If using utc_offset, tz_name should
        correspond to the desired output timezone.

    coords : tuple
        Tuple object containing the (lat,long) from which to identify a timezone.
        The default is None.

    utc_offset : int
        Fixed UTC offset in hours.


    Returns
    -------
    dt : datetime object
        Timezone-aware datetime object.

    """

    # 1. Coordinates
    #       Note: only do this if timestamp is DST-aware, don't use dt.replace(tzinfo=tz_name)
    if isinstance(coords, tuple):
        tz = pytz.timezone(tzf.TimezoneFinder().timezone_at(
            lng=coords[1], lat=coords[0]))
        dt = tz.localize(dt_naive)
    # 2. Fixed UTC offset
    elif utc_offset:
        tz = datetime.timezone(datetime.timedelta(hours=utc_offset))
        dt = dt_naive.replace(tzinfo=tz)
        # Convert to timezone
        dt = dt.astimezone(pytz.timezone(tz_name))
    # 3. Timezone name
    #       Note: only do this if timestamp is DST-aware, don't use dt.replace(tzinfo=tz_name)
    else:
        # Check if name is valid timezone
        if tz_name in pytz.all_timezones:
            # Add timezone
            tz = pytz.timezone(tz_name)
            dt = tz.localize(dt_naive)
        else:
            raise ValueError(
                'The timezone provided is not valid. To see a list of valid timezones, run pytz.alltimezones.')

    return dt
