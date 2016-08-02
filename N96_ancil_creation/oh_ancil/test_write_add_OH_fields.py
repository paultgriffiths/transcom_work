from netCDF4 import *
import numpy as np
from numpy import arange, dtype # array module from http://numpy.scipy.org
import netCDF4

"""
script to read in a file, change variable name and then write out file
"""

input_filename='/Users/ptg21/nctemp/ACTM_T42L67_OH_N96_regrid.nc'
output_filename='/Users/ptg21/nctemp/ACTM_T42L67_OH_N96_regrid_var_change.nc'

# get init data
input_file=netCDF4.Dataset(input_filename)

lon=input_file.variables['longitude']
lat=input_file.variables['latitude']
lev=input_file.variables['level']
time=input_file.variables['time']
oh_in=input_file.variables['NDOH']

nlats=len(lat)
nlons=len(lon)
nlevs=len(lev)
nrecs=len(time)

# open a new netCDF file for writing.
output_file = Dataset(output_filename,'w')

# create the lat and lon dimensions.
output_file.createDimension('latitude', nlats)
output_file.createDimension('longitude', nlons)

# create level dimension.
output_file.createDimension('sigma', nlevs)

# create time dimension (record,  or unlimited dimension)
output_file.createDimension('time', None)

# Define the coordinate variables. They will hold the coordinate
# information,  that is,  the latitudes and longitudes.
# Coordinate variables only given for lat and lon.

lats = output_file.createVariable('latitude', dtype('float32').char, ('latitude', ),  fill_value='-9999')
setattr(lats, 'long_name',  'nodal latitude')
setattr(lats, 'standard_name',  'latitude')
setattr(lats, 'units', 'degrees_north')

lons = output_file.createVariable('longitude',dtype('float32').char,('longitude', ), fill_value='-9999')
setattr(lons, 'long_name', 'nodal longitude')
setattr(lons, 'standard_name', 'longitude')
setattr(lons, 'units', 'degrees_east')

levs = output_file.createVariable('sigma', dtype('float32').char, ('sigma', ),  fill_value='-9999')
setattr(levs, 'long_name',  'sigma levels')
setattr(levs, 'standard_name',  'sigma')
setattr(levs, 'units', 'level')
setattr(levs, 'valid_min', '1e-5')
setattr(levs, 'valid_max', '1.0')


# write data to coordinate vars.
lats[:] = input_file.variables['latitude']
lons[:] = input_file.variables['longitude']
levs[:] = input_file.variables['level']
# create the pressure and temperature variables
oh_out = output_file.createVariable('OH', dtype('float32').char, ('time', 'sigma', 'latitude', 'longitude'), fill_value='-999')
oh_out[:]=oh_in

setattr(oh_out, 'long_name', 'OH Concentration / cm-3')
setattr(oh_out, 'standard_name', 'OH conc ')
setattr(oh_out, 'units', 'molecules cm -3')
setattr(oh_out, 'valid_min', '0.0')
setattr(oh_out, 'valid_max', '1e12')

# close the file.
output_file.close()


