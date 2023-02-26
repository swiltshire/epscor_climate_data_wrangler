# loads each processed geotiff raster file and saves as csv for use in cell-based r rothc model

import rioxarray
import pandas
import numpy as np
import numpy.lib.recfunctions as rfn
import matplotlib.pyplot as plt

# set params
gcm = 'ccsm4'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
vars = ['P', 'Tmin', 'Tmax']
startyr = 1950
endyr = 2099
max_rows = 116776069 # use 116776069 for all lines (65311 total cells, 1788 months)
gen_key = False

if gen_key:
    key_data = np.loadtxt('processed_data/' + gcm + '_' + vars[0] + '_' + str(startyr) + '-' + str(endyr) + '_data.csv',
                           delimiter=',', skiprows=1, max_rows=65311, usecols=[1, 2])
    with open("processed_data/cell_key.csv", "w") as f:
        f.write('cell_id,lat,lon\n')
        for each_id, row in zip(range(65311), key_data):
            line = "%d," % each_id + ",".join(format(x, "0.8f") for x in row) + "\n"
            f.write(line)

else:
    cell_ids = np.tile(np.arange(65311), 1788)[:max_rows]  # init array with cell ids
    months = np.repeat(np.arange(1788), 65311)[:max_rows] # init array with months (as int)
    for var in vars:
        infile = 'processed_data/' + gcm + '_' + var + '_' + str(startyr) + '-' + str(endyr) + '_data.csv'

        if var == vars[0]:
            comb_data = np.loadtxt(infile, delimiter=',', skiprows=1, max_rows=max_rows, usecols=[3]).reshape((-1, 1))
        else:
            data = np.loadtxt(infile, delimiter=',', skiprows=1, max_rows=max_rows, usecols=[3]).reshape((-1, 1))
            comb_data = np.concatenate((comb_data, data), axis = 1)

    with open('processed_data/' + gcm + '_' + str(startyr) + '-' + str(endyr) + '_data_comb.csv', "w") as f:
        f.write(','.join(['cell_id', 'month'] + vars) + '\n')
        for each_id, each_month, row in zip(cell_ids, months, comb_data):
            line = "%d," % each_id + "%d," % each_month + ",".join(format(x, "0.8f") for x in row) + "\n"
            f.write(line)

