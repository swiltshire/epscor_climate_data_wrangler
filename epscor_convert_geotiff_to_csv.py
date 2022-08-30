# loads each processed geotiff raster file and saves as csv for use in cell-based r rothc model

import rioxarray
import pandas
import numpy as np
import matplotlib.pyplot as plt

# set params
gcm = 'mri-cgcm3'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
var = 'P'  # 'P', 'Tmin', 'Tmax'
startyr = 1950
endyr = 2099

infile = 'processed_data/' + gcm + '_' + var + '_' + str(startyr) + '-' + str(endyr) + '_raster.tif'
outfile = 'processed_data/' + gcm + '_' + var + '_' + str(startyr) + '-' + str(endyr) + '_data.csv'

rds = rioxarray.open_rasterio(infile)
rds = rds.squeeze().drop("spatial_ref").drop("band")
rds.name = "data"
df = rds.to_dataframe().reset_index()
df.to_csv(outfile, index=False)
