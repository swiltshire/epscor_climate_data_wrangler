# loads individual csvs for each cell in study area, and saves average data across all cells to run model on full sa

import numpy as np
import pandas as pd

# set params
gcm = 'mri-cgcm3'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
startyr = 1950
endyr = 2099
in_dir = 'processed_data/' + gcm + '_' + str(startyr) + '-' + str(endyr) + '_by_cell/'

sim_styr_i = 2022-1950-1
sim_endyr_i = 2099-1950-1

with open("processed_data/cell_ids_final.txt", "r") as cell_id_file:
    cell_ids = cell_id_file.read().splitlines()

# cell_ids = cell_ids[10000:10100] # subset for testing, otherwise comment out

with open("processed_data/cell_clim_stats_" + gcm + ".csv", "w") as out_dat:
    out_dat.write("cell_id,2022_t,2099_t,t_diff,2022_p,2099_p,p_diff,\n")
    for cell_id in cell_ids:
        cell_dat = pd.read_csv(in_dir + str(cell_id) + ".csv").iloc[:,-3:]
        first_yr_dat = cell_dat.iloc[(12*sim_styr_i):(12*sim_styr_i+12),]
        last_yr_dat = cell_dat.iloc[(12*sim_endyr_i):(12*sim_endyr_i+12),]
        first_yr_means = first_yr_dat.mean()
        last_yr_means = last_yr_dat.mean()
        first_yr_means["Tavg"] = (first_yr_means["Tmin"] + first_yr_means["Tmax"]) / 2
        last_yr_means["Tavg"] = (last_yr_means["Tmin"] + last_yr_means["Tmax"]) / 2
        out_dat.write(str(cell_id) + "," +
                      str(first_yr_means["Tavg"]) + "," +
                      str(last_yr_means["Tavg"]) + "," +
                      str(last_yr_means["Tavg"] - first_yr_means["Tavg"]) + "," +
                      str(first_yr_means["P"]) + "," +
                      str(last_yr_means["P"]) + "," +
                      str(last_yr_means["P"] - first_yr_means["P"]) + "\n"
                      )


# out_dat.to_csv("processed_data/cell_clim_stats.csv", index = False)
