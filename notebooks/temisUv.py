#!/bin/python3

'''
 Extract the 9-day TEMIS UV index forecast for a given location
 
 usage:  get_uvief_fc.py -h
 
 source: https://www.temis.nl/uvradiation/
 
'''

import numpy as np
import netCDF4
import sys
import os

import warnings
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=RuntimeWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

# ==================================================================

def GetValues(lon,lat,ncFile):
    
    ilon = getIlon(lon)
    ilat = getIlat(lat)
    
    with netCDF4.Dataset(ncFile,'r') as nc:
        
        dates = nc.groups['PRODUCT'].variables['date'][:]
        nDays = len(dates)
        
        uvief = nc.groups['PRODUCT'].variables['uvi_clear'][:,ilat,ilon]
        ozone = nc.groups['PRODUCT'].variables['ozone_column'][:,ilat,ilon]
        
    print('# TEMIS UV index forecast')
    print('# =======================')
    print('# source: https://www.temis.nl/uvradiation/')
    print('# (c) KNMI/ESA')
    print('#')
    print('# UV index [dimensionless] and ozone column [DU]')
    print('# at local solar noon for the location:')
    print('#')
    print('# lon, lat = %g, %g' % (lon,lat) )
    print('#')
    print('# YYYYMMDD  UVindex  Ozone')
    for iDay in range(0,nDays,1):
        print('  %8d   %6.3f  %5.1f' % ( dates[iDay],uvief[iDay],ozone[iDay] ) )
     
    return

# ======================           

# Conversion routines of latitude and longitude coordinates in degrees
# to grid cell indices. The index counting is 0-based, that is:
# * longitudes range from 0 (West) to 1439 (East)
# * latitudes  range from 0 (South) to 719 (North)
# The grid cells are dlon by dlat = 0.25 by 0.25 degrees

def getIlon(lon):
    dlon = 360.0/1440.0
    return int(round( ( lon + 180.0 - dlon/2.0 ) / dlon ))
def getIlat(lat):
    dlat = 180.0/720.0
    return int(round( ( lat +  90.0 - dlat/2.0 ) / dlat ))
def getLon(ilon):
    dlon = 360.0/1440.
    return dlon * ilon - 180.0 + dlon/2.0
def getLat(ilat):
    dlat = 180.0/720.0
    return dlat * ilat -  90.0 + dlat/2.0

# ==================================================================
# Main part
# ==================================================================

if __name__ == "__main__":
    
    # Configuration
    # -------------
    
    import argparse
    
    parser = argparse.ArgumentParser(description=\
       'Extract the 9-day TEMIS UV index forecast for a given location.')
    
    lonStr = 'longitude, decimal degrees in range [-180:+180]  '
    parser.add_argument('lon',metavar='LON',help=lonStr)
    
    latStr = 'latitude, decimal degrees in range [-90:+90]'
    parser.add_argument('lat',metavar='LAT',help=latStr)
    
    fileStr = 'netCDF file with the 9-day forecast'
    parser.add_argument('file',metavar='FILE',help=fileStr)
    
    args = parser.parse_args()
    
    file = args.file
    lon = float(args.lon)
    lat = float(args.lat)
    
    if ( not os.path.isfile(file) ):
        print(' *** Error: given netCDF file does not exist' )
        sys.exit(1)
    
    if ( lon > 180.0  or  lon < -180.0 ):
        print(' *** Error: longitude should be in the range [-180:+180]' )
        sys.exit(1)
    
    if ( lat >  90.0  or  lat <  -90.0 ):
        print(' *** Error: latitude should be in the range [-90:+90]' )
        sys.exit(1)
    
    # Run the process
    # ---------------
    
    GetValues(lon,lat,file)
    
    # All done
    # --------
    
    sys.exit(0)
    