import cfgrib
import xarray as xr
import iris
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def main():
    variables = ['TG', 'PSG', 'TRG', 'UG', 'VG']

    lats = np.arange(-90,91,1)
    lons = np.arange(0,360,1)

    year0,month0,day0,hora0=sys.argv[1].split('-')
    year1,month1,day1,hora1=sys.argv[2].split('-')

    os.system('rm -r interpolated_data')
    os.system('mkdir interpolated_data')

    filelist=[f'fnl_{year0}{month0}{day0}_{hora0}_00.grib2',f'fnl_{year1}{month1}{day1}_{hora1}_00.grib2']
    for idx,file in enumerate(filelist):
        for var in variables:
            grb_data = read_grib2(f'./grib-data/{file}',var)
            grb2nc(grb_data,f'./{var}.nc')
            nc = read_nc(f'{var}.nc')
            nc_selected = select_data(nc)
            nc_interpolated = interpolate(lats, lons,nc_selected)
            print(f'Saving {var}{idx}')
            iris.save(nc_interpolated,f'./interpolated_data/interpolated_{var}{idx}.nc')
    os.system('rm *G.nc')

def grbvar2ncvar(grib_var):
    if grib_var == 'Temperature':
        return 'TG'
    elif grib_var == 'U component of wind':
        return 'UG'
    elif grib_var == 'V component of wind':
        return 'VG'
    elif grib_var == 'Relative humidity':
        return 'TRG'
    elif grib_var == 'Geopotential height':
        return 'PSG'
    else:
        return None
def ncvar2grbvar(grib_var):
    if grib_var == 'TG':
        return 'Temperature'
    elif grib_var == 'UG':
        return 'U component of wind'
    elif grib_var == 'VG':
        return 'V component of wind'
    elif grib_var == 'TRG':
        return 'Relative humidity'
    elif grib_var == 'PSG':
        return 'Geopotential height'
    else:
        return None

def read_grib2(path:str, var:str):
    return xr.load_dataset(path, engine='cfgrib', filter_by_keys={'typeOfLevel': 'isobaricInhPa','name':ncvar2grbvar(var)})

def grb2nc(xr_grb, path_to:str):
    return xr_grb.to_netcdf(path=path_to)

def read_nc(path:str):
    return iris.load_cube(path)

def select_data(nc_grid):
    levels = [30,100,200,300,500,700,850,925]
    query = iris.Constraint(air_pressure = lambda cell: cell in levels)
    return nc_grid.extract(query)

def interpolate(lats, lons,grid):
    new_coords = [('longitude', np.arange(0, 360, 5.625)),
                  ('latitude',  np.array([-85.761,-80.269,-74.745,-69.213,-63.679,-58.143,-52.607,-47.070,-41.532,-35.995,-30.458,-24.920,-19.382,-13.844,-8.307,-2.769,2.769,8.307,13.844,19.382,24.920,30.458,35.995,41.532,47.070,52.607,58.143,63.679,69.213,74.745,80.269,85.761]))]
    return grid.interpolate(new_coords,iris.analysis.Linear())

if __name__ == "__main__":
    main();