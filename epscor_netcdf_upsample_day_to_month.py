# processes raw epscor netCDF files (1 yr each, daily tsteps) and computes averages by month for each cell
# necessary to load cdf data into memory in chunks to prevent memory overflow

import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt

# set params
gcm = 'mri-cgcm3'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
var = 'Tmax'  # 'P', 'Tmin', 'Tmax'
startyr = 1950
endyr = 2099
nyrs_chunk = 15  # chunk size in years, 15 is typically good (memory overflow if load all years)
save_mo_avg_data = True
plot_mo_avg_data_full_sa = True

# basic time calcs
nyrs = endyr - startyr
startyr_i = startyr - 1950

# make multi-file netCDF dataset
ds = nc.MFDataset('data/' + gcm + '/cmip5.bcca.' + gcm + '.1.rcp45.30arcsec.idw.*_' + var + '.nc')

print('Loading first chunk')
var_dict = {"Tmin": "Minimum_Temperature", "Tmax": "Maximum_Temperature", "P": "Precipitation"}
data = ds.variables[var_dict[var]][range(startyr_i, startyr_i + nyrs_chunk)]  # load first chunk

mo_avg_data = np.zeros(shape=(nyrs*12, data.shape[2], data.shape[3]))  # init numpy array of correct size (nyrs*12, nxccords, nycoords)

mo_breaks = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]  # day nums to divide yr into mos

chunk_i = 0
for yr in range(nyrs):
    if (yr > 0) & (yr % nyrs_chunk == 0):
        print('Loading new chunk')
        data = ds.variables[var_dict[var]][range(yr, min(yr+nyrs_chunk, nyrs)), :, :, :]  # load next chunk
        chunk_i += 1
    print('Processing year ' + str(yr+1))
    for mo in range(12):
        days_in_mo = range(mo_breaks[mo], mo_breaks[mo+1])
        mo_data = data[yr-nyrs_chunk*chunk_i, days_in_mo]  # all daily values within month
        mo_avg_data[yr * 12 + mo] = np.ma.mean(mo_data, axis=0)  # record monthly averages in np array
        # print(np.ma.mean(mo_avg))  # to sanity check monthly average data

# save monthly average combined data
if save_mo_avg_data:
    np.save('processed_data/' + gcm + '_' + var + '_mo_avg_comb_' + str(startyr) + '-' + str(startyr+nyrs) + '.npy',
            mo_avg_data)

# quick plot of full study area average for sanity check
if plot_mo_avg_data_full_sa:
    whole_sa_mo_avg_data = np.mean(mo_avg_data, axis=(1, 2))
    tvals = np.arange(startyr, startyr + nyrs, 1/12)
    plt.plot(tvals, whole_sa_mo_avg_data)
    plt.show()

print("Done")
