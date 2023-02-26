# processes numpy array with metadata from netCDFs and exports as geotiff for use in GIS
# instructions to install gdal: https://gis.stackexchange.com/questions/28966/python-gdal-package-missing-header-file-when-installing-via-pip

import netCDF4 as nc
import numpy as np
from osgeo import gdal
from osgeo import osr

# set params
gcm = 'mri-cgcm3'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
var = 'Tmax'  # 'P', 'Tmin', 'Tmax'
startyr = 1950
endyr = 2099

# just load one year of CDF file to get lat/lon
ds = nc.Dataset('data/' + gcm + '/' + 'cmip5.bcca.' + gcm + '.1.rcp45.30arcsec.idw.1950_' + var + '.nc')
lat = ds.variables['latitude'][:]
lon = ds.variables['longitude'][:]

mo_avg_data = np.load('processed_data/' + gcm + '_' + var + '_mo_avg_comb_' + str(startyr) + '-' + str(endyr) + '.npy')

# make it smaller for testing
# lat = lat[1:50]
# lon = lon[1:50]
# mo_avg_data = mo_avg_data[:, 1:50, 1:50]

xmin, ymin, xmax, ymax = [lon.min(), lat.min(), lon.max(), lat.max()]
nyrs, nrows, ncols = np.shape(mo_avg_data)
xres = (xmax-xmin) / float(ncols)
yres = (ymax-ymin) / float(nrows)

geotransform = (xmin-360, xres, 0, ymax, 0, -yres)
# That's (top left x, w-e pixel resolution, rotation (0 if North is up),
#         top left y, rotation (0 if North is up), n-s pixel resolution)

# instructions: https://lists.osgeo.org/pipermail/gdal-dev/2008-June/017338.html

outfile = 'processed_data/cell_key_raster.tif'

output_raster = gdal.GetDriverByName('GTiff').Create(outfile, ncols, nrows, 1, gdal.GDT_Float32)  # Open the file
output_raster.SetGeoTransform(geotransform)  # Specify its coordinates
srs = osr.SpatialReference()                 # Establish its coordinate encoding
srs.ImportFromEPSG(4326)                     # This one specifies WGS84 lat lon
# srs.ImportFromEPSG(4269)                     # This one specifies NAD83 lat lon
# srs.ImportFromEPSG(5070)                     # This one specifies ESRI:102039 - USA_Contiguous_Albers_Equal_Area_Conic_USGS_version - Projected
output_raster.SetProjection(srs.ExportToWkt())   # Exports the coordinate system to the file

# write each band of raster
# for yr_i in range(nyrs):
#     output_raster.GetRasterBand(yr_i+1).WriteArray(mo_avg_data[yr_i])

cell_ids = np.arange(65311).reshape(nrows, ncols)
output_raster.GetRasterBand(1).WriteArray(cell_ids)

output_raster.FlushCache()  # output raster and close file

print("Done")
