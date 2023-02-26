# splits each large csv (with data for all cells) into individual csvs for each cell, for use in batch runs on cheyenne

import numpy as np
import os

# set params
gcm = 'ccsm4'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
startyr = 1950
endyr = 2099
max_cells = 65311
max_mos = 1788
max_rows = 116776069  # use 116776069 for all lines (65311 total cells, 1788 months)

chunk_sz_mos = 100
n_chunks = int(np.ceil(max_mos / chunk_sz_mos))
chunk_ids = np.arange(1, n_chunks+1)

# to select all cells
cell_ids = np.arange(max_cells)
# to select only cells in SA
# with open('processed_data/cell_ids_in_sa.csv', 'r') as in_f:
#     cell_ids_in_sa = [int(line.split()[0]) for line in in_f]
# cell_ids = cell_ids_in_sa[0:2]
# to select a smaller number of cells (for testing)
# cell_ids = np.arange(10)


# split original file into chunks of n months using shell command:
# "tail -n +2 mri-cgcm3_1950-2099_data_comb.csv | split --numeric-suffixes=1 --additional-suffix=.csv -l6531100 - mri-cgcm3_1950-2099_data_comb_"
# where num. lines argument = max_cells * chunk_sz_mos

new_dir = 'processed_data/' + gcm + '_' + str(startyr) + '-' + str(endyr) + '_by_cell'
cur_dir = os.getcwd()
fin_dir = os.path.join(cur_dir, new_dir)
if not os.path.exists(fin_dir):
    os.makedirs(fin_dir)

# fetch header and write
with open('processed_data/' + gcm + '_' + str(startyr) + '-' + str(endyr) + '_data_comb.csv', "r") as in_f:
    print('Writing headers')
    hdr = in_f.readline()
    for cell_id in cell_ids:
        np.savetxt(new_dir + '/' + str(cell_id) + '.csv', [hdr[8:]], delimiter=',', fmt="%s", newline='')

mo = 0
for chunk in chunk_ids:
    print('PROCESSING CHUNK ' + str(chunk) + ' OF ' + str(n_chunks))
    in_f_name = 'processed_data/' + gcm + '_' + str(startyr) + '-' + str(endyr) + '_data_comb_' + "%02d" % (chunk,) + '.csv'
    with open(in_f_name, "r") as in_f:
        cell_dat = np.empty([max_cells, min(chunk_sz_mos, max_mos-mo-1), 4], dtype=object)
        for line in in_f:
            ln_sp = line.split(',')
            cell_dat[int(ln_sp[0])][int(ln_sp[1]) - chunk_sz_mos * (chunk - 1)] = (ln_sp[1], ln_sp[2], ln_sp[3], ln_sp[4])

            if mo != int(ln_sp[1]):
                if mo % 10 == 0:
                    print('Reading month ' + ln_sp[1])
                mo = int(ln_sp[1])

    for cell_id in cell_ids:
        with open(new_dir + '/' + str(cell_id) + '.csv', 'ab') as out_f:
            if cell_id % 1000 == 0:
                print('Writing cell ' + str(cell_id))
            out_txt = [",".join(i) for i in cell_dat[cell_id].astype(str)]
            np.savetxt(out_f, out_txt, delimiter=',', fmt="%s", newline='')



