#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'brynmorgan@ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2021'

__license__ = 'MIT'
__date__ = 'Sat 25 Sep 21 16:06:29'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           ortho.py
Compatibility:  Python 3.10.0
Description:    Description of what program does

Requires:       numpy, xarray, rioxarray, richdem

Notes:          Copied from ecoflydro library (pre-release). Not intended for 
                solo use.

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        brynmorgan@ucsb.edu
Copyright:      (c) Bryn Morgan 2021

"""


# IMPORTS

import os
import numpy as np
import re

import xarray as xr
import rioxarray as rio
import richdem as rd

from utils_ortho import filename_to_dt


class Orthoimage():
    """

    """
    def __init__(self, file, config):
        """
        Parameters
        ----------
        config : configparser.SectionProxy
            Contains the 'ortho' section of the config object.
        """
        # filename
        self.filename = file
        # _config
        self._config = config
        # timestamp
        self.timestamp = None
        # _init
        self._init = False
    
    def __eq__(self, other):
        if isinstance(other, Orthoimage):
            return self.filename == other.filename

    def __gt__(self, other):
        if isinstance(other, Orthoimage):    
            return self.get_timestamp() > other.get_timestamp()
    
    def __repr__(self):
        class_name = type(self).__name__
        return '{}(file="{}")'.format(class_name,self.filename)

    def get_timestamp(self):
        raise NotImplementedError

    @staticmethod
    def import_ortho():
        """
        
        """
        raise NotImplementedError

    def is_inited(self):
        """
        Check whether object has been initialized.

        Returns
        -------
        boolean
            Boolean based on self._init
        """
        return self._init

class MicaSenseOrtho(Orthoimage):

    bands = {'B': 0, 'G': 1, 'R': 2, 'R-E': 3, 'NIR': 4, 'TIR': 5}

    def __init__(self, file, config, dem_file=None):

        super().__init__(file,config)
        # name
        self.name = os.path.splitext(os.path.basename(self.filename))[0]
        # flight_id
        self.flight_id = self.get_flight_id()
        # timestamp
        self.timestamp = self.get_timestamp()

        # dem_file
        # TODO: Not this.
        if not dem_file:
            self.dem_file = os.path.join(
                os.path.dirname(os.path.realpath(self.filename)),
                'DEM',
                # os.path.splitext(os.path.basename(self.filename))[0] + '_DEM.tif'
                self.name + '_DEM.tif'
            )
            self.dtm_file = os.path.join(
                os.path.dirname(os.path.realpath(self.filename)),
                'DTM',
                # os.path.splitext(os.path.basename(self.filename))[0] + '_DTM.tif'
                self.name + '_DTM.tif'
            )

        else:
            self.dem_file = dem_file

        # raster
        # self.raster = None

        # ortho_array
        self.ortho_array = None

        # dem
        self.dem = None
        self._dem_rd = None
        # dtm
        self.dtm = None
        # chm
        self.chm = None

    def init(self):

        # raster, ortho_array
        # self.raster,self.ortho_array = self.import_ortho(self.filename)
        self.ortho_array = self.import_ortho(self.filename)

        # dem
        if os.path.isfile(self.dem_file):
            self.dem = self.import_dem(self.dem_file)
            # self._dem_rd = self.import_dem_rd(self.dem_file)
        if os.path.isfile(self.dtm_file):
            self.dtm = self.import_dem(self.dtm_file)
        
        # Set init flag
        self._init = True
    

    def get_flight_id(self):
        # return re.findall(r"[0-9]\w+",os.path.splitext(os.path.basename(self.filename))[0])[0]
        return re.findall(r"[0-9]\w+", self.name)[0]


    def get_timestamp(self):
        """
        Get the timestamp of a FlirImageFolder

        Parameters
        ----------
        config : configparser.SectionProxy
            Contains the 'tir' section of the config object.
        """
        if not self.timestamp:
            # timestamp
            dt = filename_to_dt(
                self.flight_id,
                # CONFIG_USE
                dt_format=self._config.get('dt_format', '%Y-%m-%d %H:%M:%S.%f'),
                tz_name=self._config.get('tz', 'America/Los_Angeles')
            )
            self.timestamp = dt
            return dt
        else:
            return self.timestamp


    @staticmethod
    def import_ortho(file, bands=None, masked=True, nodata=65535., project=False, crs=None):
        """
        Import an orthophoto raster as a DataArray

        Parameters
        ----------
        file : str
            Filename of raster to be imported

        bands : list, str, or int, optional
            Band name or list of bandnames to be imported. The default (None) is 
            to import all bands of the image.

        masked : bool, optional
            Whether or not to mask no data values, by default True. 

        project : bool, optional
            Whether or not to project the array, by default True.
            NOTE: I *think* what this does (rio.reproject_match) is simply re-shape 
            the input array to the appropriate shape (rather than leave it as a 1-D
            collection of pixels/numbers). Need to play with this bc this step is 
            time-consuming.

        crs : rasterio.crs.CRS, optional
            The CRS projection of the dataset, by default rasterio.crs.CRS.from_epsg(32610).
            TODO: This can be determined from the array, but I get an error saying it
            requires pyproj3+, and I don't want to upgrade and break other things.
            For now, I'm using the projection that I know it is for UTM Zone 10N.

        Returns
        -------
        arr : xarray.DataArray
            Raster data as a DataArray.
        """
        # Read in data
        arr = rio.open_rasterio(file, masked=masked)

        # Shape into the right projection
        if project:

            arr.rio.reproject_match(arr)
            # Apply coordinate projection (not sure this does anything)
            if not crs:
                crs = arr.rio.crs
            arr = arr.rio.reproject(crs)

        # Select desired bands
        if bands:
            # If a list of band names is passed, select those bands
            if isinstance(bands,list):
                arr = arr.sel(band=bands)
            # Otherwise (i.e. if a single band is passed), select the band and 
            # reduce to 2-D array (remove the 'band' dimension).
            else:
                arr = arr.sel(band=bands).drop('band')
        
        # Check whether NoData value has been set, and if not, set to given value.
        if not arr.rio.encoded_nodata:
            arr = MicaSenseOrtho.set_nodata(arr, nodata=nodata)

        return arr


    @staticmethod
    def resample_res(in_array, proj_array):
        """
        Resample the resolution of a DataArray.

        Parameters
        ----------
        in_array : xarray.DataArray
            Array to be resampled
        proj_arr : xarray.DataArray
            DataArray to which to project the input array.

        Returns
        -------
        arr_resamp : xarray.DataArray
            Resampled array.

        TODO: Consider using rioxarray methods instead:
            arr_resamp = in_array.rio.reproject_match(proj_array)
            arr_resamp = arr_resamp.assign_coords({'x': in_array.x, 'y': in_array.y})
        This updates the resolution (etc.) and maintains handling of raster stuff.
        The downside is that it doesn't handle NoData well, but not an issue if 
        subsequently performing operations with an array with proper NoData.

        """
        arr_resamp = in_array.interp(x=proj_array.x, y=proj_array.y)

        return arr_resamp


    def proj_to_dem(self):
        """
        Project ortho_array to the resolution of the DEM.

        Returns
        -------
        arr_resamp : xarray.DataArray
            ortho_array resampled to the resolution of the DEM.
        """
        
        # proj_array = self.import_ortho(self.dem_file, masked=False, project=False)

        arr_resamp = self.resample_res(self.ortho_array, self.dem)

        return arr_resamp




    @staticmethod
    def set_nodata(array, nodata=65535.0):
        """
        Set NoData value of ortho_array + mask (set nan).

        Parameters
        ----------
        nodata : float, optional
            The value to be set as NoData (nan), by default 65535.0.

        Yields
        -------
        self.ortho_array with masked NoData values (as nan).
            
        """
        # First, check to see if the array has a nodata value
        if array.rio.nodata:
            nodata = array.rio.nodata
        # Set nodata value
        array.rio.write_nodata(nodata, inplace=True)
        # ortho_array = ortho_array.where(ortho_array != nodata)
        array = array.where(array != array.rio.nodata)
        array.rio.write_nodata(array.rio.nodata, encoded=True, inplace=True)

        return array


    def calc_ndvi(self):
        """
        Calculates NDVI.

        Returns
        -------
        ndvi : xarray.DataArray
            NDVI array.
        """

        red = self.ortho_array[self.bands.get('R')]
        nir = self.ortho_array[self.bands.get('NIR')]

        ndvi = (nir - red) / (nir + red)

        return ndvi
    
    def get_temperature(self):

        T_s = self.ortho_array[self.bands.get('TIR')] / 100

        return T_s


    @staticmethod
    def import_dem(dem_file):
        """
        Imports a DEM raster to an xarray.DataArray.

        Parameters
        ----------
        dem_file : str
            Filename of DEM file.

        Returns
        -------
        [type]
            [description]
        """
        # Import DEM
        dem = MicaSenseOrtho.import_ortho(dem_file, bands=1)

        return dem


    def generate_chm(self, mask_neg=True, set_chm=True):
        """
        Calculate the canopy height model (CHM) from the DEM and DTM.

        Parameters
        ----------
        mask_neg : bool, optional
            Whether to mask negative values (i.e. ground points above the DTM),
            by default True.

        Returns
        -------
        chm : xarray.DataArray
            Canopy height model.
        """
        # Align coordinates of DTM and DEM
        dtm = self.dtm.interp(
            x=self.dem.x, y=self.dem.y, method='nearest'
        )
        # Calculate canopy height model
        chm = self.dem - dtm

        # Set any negative values to 0
        # chm = chm.where(chm >= 0, other=0)
        if mask_neg:
            chm = xr.where(chm < 0, 0, chm)

        chm.rio.set_crs(self.dem.rio.crs)
        
        if set_chm:
            self.chm = chm

        return chm


    def get_hillshade(self, file=None):
        """
        Import hillshade file + align with DEM.

        Parameters
        ----------
        file : str, optional
            Name of hillshade file. By default, get filename and path relative to
            ortho filename.

        Returns
        -------
        hillshade : xarray.DataArray
            Hillshade array.
        """

        if file is None:
            # Get name hillshade file for flight
            file = os.path.join(
                os.path.dirname(os.path.realpath(self.filename)),
                'Hillshade',
                self.name + '_Hillshade.tif'
            )
        # Import hillshade file
        hillshade = self.import_ortho(file, bands=1)
        # hillshade = hillshade.reindex_like(ortho_resamp, method='nearest',tolerance=0.01)
        if hillshade.shape != self.dem.shape:
            hillshade = hillshade.interp(x=self.dem.x, y=self.dem.y)
        # Check if dimensions match, but coordinates do not.
        # NOTE: Added 15 may 2023 bc at least one flight has mismatched coordinates in y 
        # (hillshade y-coords have 1 less decimal places than dem). Need robust solution.
        elif (hillshade.y == self.dem.y).sum() != self.dem.shape[0]:
            hillshade = hillshade.reindex_like(self.dem, method='nearest')

        return hillshade


    @staticmethod
    def import_dem_rd(dem_file):
        """
        Import a DEM as a richdem.rdarray. 
        Intended for use in calculation of slope and aspect.

        Parameters
        ----------
        dem_file : str
            Filename of DEM file to be loaded.

        Returns
        -------
        dem_rd : richdem.rdarray
            Contains DEM data.
        """
        dem_rd = rd.LoadGDAL(dem_file)

        return dem_rd



    def calc_slope(self, unit='radians'):
        """
        Calculate the slope of a surface from the DEM.

        Parameters
        ----------
        dem : richdem.rdarray 
            DEM [m].
        unit : str, optional
            Output unit. The options are 'radians' (default) or 'degrees'.

        Returns
        -------
        slope : richdem.rdarray
            Slope of the surface [radians or degrees].
        """

        if unit == 'radians':
            slope = rd.TerrainAttribute(self._dem_rd, 'slope_radians')
        else:
            slope = rd.TerrainAttribute(self._dem_rd, 'slope_degrees')

        nodata = slope.no_data

        slope = xr.DataArray(
            slope,
            coords = {'x': self.dem.x,'y': self.dem.y},
            dims = ['y', 'x']
        )

        slope = self.set_nodata(slope, nodata = nodata)

        return slope


    def calc_aspect(self, unit='radians'):
        """
        Calculate the aspect (orientation of a slope from N) of a surface from a DEM.

        Parameters
        ----------
        dem : richdem.rdarray
            DEM [m].
        unit : str, optional
            Output unit. The options are 'radians' (default) or 'degrees'.

        Returns
        -------
        aspect : richdem.rdarray
            Aspect of the surface [radians or degrees].
        """

        if unit == 'radians':
            aspect = np.radians(rd.TerrainAttribute(self._dem_rd, 'aspect'))
            nodata = np.radians(aspect.no_data)
        else:
            aspect = rd.TerrainAttribute(self._dem_rd, 'aspect')
            nodata = aspect.no_data

        aspect = xr.DataArray(
            aspect,
            coords = {'x': self.dem.x,'y': self.dem.y},
            dims = ['y', 'x']
        )

        aspect = self.set_nodata(aspect, nodata = nodata)

        return aspect








