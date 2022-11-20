import numpy as np
import netCDF4 as nc
import os
import sys


def main():
    start = sys.argv[1].split("-")
    final = sys.argv[2].split("-")

    print(
        f"Creating initial condition for date0: {start[0]}/{start[1]}/{start[2]}/{start[3]}:00  and date1: {final[0]}/{final[1]}/{final[2]}/{final[3]}:00"
    )
    #os.system("rm -r ./grib-data/*")
    #   os.system(
    #       f"python3 download.py {start[0]}-{start[1]}-{start[2]}-{start[3]} {final[0]}-{final[1]}-{final[2]}-{final[3]}"
    #   )
    os.system(
        f"python3 grib2speedy.py {start[0]}-{start[1]}-{start[2]}-{start[3]} {final[0]}-{final[1]}-{final[2]}-{final[3]}"
    )
    src_nc = "./initial_condition_structure.nc"
    trg_nc = "./initial_condition.nc"
    create_file_from_source(src_nc, trg_nc)
    #os.system("rm -r *.npy")


def change(var):
    vari = 0
    if var == "UG0":
        vari = np.load("UG0.npy")
    if var == "VG0":
        vari = np.load("VG0.npy")
    if var == "TG0":
        vari = np.load("TG0.npy")
    if var == "TRG0":
        vari = np.load("TRG0.npy")
    if var == "PSG0":
        vari = np.load("PSG0.npy")
    if var == "UG1":
        vari = np.load("UG1.npy")
    if var == "VG1":
        vari = np.load("VG1.npy")
    if var == "TG1":
        vari = np.load("TG1.npy")
    if var == "TRG1":
        vari = np.load("TRG1.npy")
    if var == "PSG1":
        vari = np.load("PSG1.npy")
    if var == "longitude":
        vari = np.load("longitude.npy")
    if var == "latitude":
        vari = np.load("latitude.npy")
    if var == "level":
        vari = np.load("level.npy")
    return vari


def create_file_from_source(src_file, trg_file):
    trg = nc.Dataset(trg_file, mode="w")
    src = nc.Dataset(src_file, mode="a")
    # Create the dimensions of the file
    for name, dim in src.dimensions.items():
        trg.createDimension(name, len(dim))
        # if len(dim)==64:
        #     # print(f'dim: {len(dim)}=>{96}')
        #     trg.createDimension(name, 96)
        # elif len(dim)==32:
        #     # print(f'dim: {len(dim)}=>{32}')
        #     trg.createDimension(name, 48)
        # else:
        #     # print(f'dim: {len(dim)}=>{len(dim)}')
        #     trg.createDimension(name, len(dim))
    # Copy the global attributes
    trg.setncatts({a: src.getncattr(a) for a in src.ncattrs()})

    # Create the variables in the file
    for name, var in src.variables.items():
        # # Copy the variable attributes
        print(name)
        print(var.dimensions)
        trg.createVariable(name, var.dtype, var.dimensions)
        trg.variables[name].setncatts({a: var.getncattr(a) for a in var.ncattrs()})
        # # Copy the variables values (as 'f4' eventually)
        if (
            name == "UG0"
            or name == "VG0"
            or name == "TG0"
            or name == "PSG0"
            or name == "TRG0"
            or name == "UG1"
            or name == "VG1"
            or name == "TG1"
            or name == "PSG1"
            or name == "TRG1"
            or name == "longitude"
            or name == "latitude"
            or name == "level"
        ):
            trg.variables[name][:] = change(name)
        else:
            print(name)
            trg.variables[name][:] = src.variables[name][:]

    # Save the file
    trg.close()
    src.close()


if __name__ == "__main__":
    main()
