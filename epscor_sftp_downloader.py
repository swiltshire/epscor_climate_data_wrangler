# connects to epscor compute server using sftp and downloads climate files

import pysftp


def main():

  host = 'epscor-pascal.uvm.edu'
  port = 22
  username = input("Enter username for EPSCoR server: ")
  password = input("Enter password for " + username + ": ")

  try:
    conn = pysftp.Connection(host=host, port=port, username=username, password=password)
    print("Connection established successfully")
  except:
    print('Failed to establish connection to EPSCoR server, make sure VPN is on and password is correct')

  basedir = '/epscorfs/data/RACC_Climate_Projections/ensembles/'

  # current_dir = conn.pwd
  # print('Current working directory is: ', current_dir)
  # print(conn.listdir())

  gcm = 'ccsm4'  # "ccsm4", "miroc-esm", "noresm1-m", "mri-cgcm3"
  var = 'Tmax'  # 'P', 'Tmin', 'Tmax'
  startyr = 1950
  endyr = 2099

  for yr in range(startyr, endyr):
    conn.chdir(basedir + 'cmip5.bcca.' + gcm + '.1.rcp45/cmip5.bcca.' + gcm + '.1.rcp45.30sec.idw/out/')
    filename = 'cmip5.bcca.' + gcm + '.1.rcp45.30arcsec.idw.' + str(yr) + '_' + var + '.nc'
    print('Downloading ' + filename + ': ' + str(round(conn.stat(filename).st_size/1000000)) + ' MB')
    conn.get(filename, localpath = './data/' + gcm + '/' + filename)


if __name__ == "__main__":
    main()