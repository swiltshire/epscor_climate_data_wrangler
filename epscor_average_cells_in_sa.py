# loads individual csvs for each cell in study area, and saves average data across all cells to run model on full sa

import numpy as np
import pandas as pd

# set params
gcm = 'mri-cgcm3'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
startyr = 1950
endyr = 2099
in_dir = 'processed_data/' + gcm + '_' + str(startyr) + '-' + str(endyr) + '_by_cell/'

with open("processed_data/cell_ids_final.txt", "r") as cell_id_file:
    cell_ids = cell_id_file.read().splitlines()

# cell_ids = cell_ids[0:2] # subset for testing, otherwise comment out

for cell_id in cell_ids:
    gcm_dat_df_cell = pd.read_csv(in_dir + str(cell_id) + ".csv").iloc[:,-3:]
    gcm_dat_df_cell_scaled = gcm_dat_df_cell.div(len(cell_ids))
    if cell_id == cell_ids[0]:
        out_dat = gcm_dat_df_cell_scaled
    else:
        out_dat = out_dat + gcm_dat_df_cell_scaled

out_dat.insert(0, "month", range(0, 1788))
print(out_dat)

out_dat.to_csv("processed_data/" + gcm + '_' + str(startyr) + '-' + str(endyr) + "_sa_avg.csv", index = False)
