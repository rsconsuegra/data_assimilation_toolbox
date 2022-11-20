import sys
import pygrib
import numpy as np
import xarray as xr
import warnings


def fxn():
    warnings.warn("deprecated", DeprecationWarning)


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

year0, month0, day0, hora0 = sys.argv[1].split("-")
year1, month1, day1, hora1 = sys.argv[2].split("-")
X_speedy_lon = np.arange(0, 360, 5.625)
Y_speedy_lat = np.array(
    [
        -85.761,
        -80.269,
        -74.745,
        -69.213,
        -63.679,
        -58.143,
        -52.607,
        -47.070,
        -41.532,
        -35.995,
        -30.458,
        -24.920,
        -19.382,
        -13.844,
        -8.307,
        -2.769,
        2.769,
        8.307,
        13.844,
        19.382,
        24.920,
        30.458,
        35.995,
        41.532,
        47.070,
        52.607,
        58.143,
        63.679,
        69.213,
        74.745,
        80.269,
        85.761,
    ]
)
levels = [30, 100, 200, 300, 500, 700, 850, 925]
filenames = [
    f"fnl_{year0}{month0}{day0}_{hora0}_00.grib2",
    f"fnl_{year1}{month1}{day1}_{hora1}_00.grib2",
]

##(181,360)->(32,64)
def merge_grids(Y_speedy_lat, X_speedy_lon, grb):
    vals_grb = np.asarray(grb.values)
    lat, lon = grb.latlons()
    lat = np.array(lat[:, 0])
    lon = np.array(lon[0])
    data_xr = xr.DataArray(vals_grb, coords={"y": lat, "x": lon}, dims=["y", "x"])
    data_int = data_xr.interp(x=X_speedy_lon, y=Y_speedy_lat, method="cubic")
    return data_int


UG0 = []
UG1 = []
VG0 = []
VG1 = []
TG0 = []
TG1 = []
TRG0 = []
TRG1 = []
for idx, file in enumerate(filenames):
    print(f"Reading file: {file}")
    grbs = pygrib.open(f"grib-data/{file}")
    for grb in grbs:
        if "Pressure" in grb["name"] and "heightAboveGround" == grb.typeOfLevel:
            if idx == 0:
                PSG0 = [merge_grids(Y_speedy_lat, X_speedy_lon, grb)]
            else:
                PSG1 = [merge_grids(Y_speedy_lat, X_speedy_lon, grb)]
        if "isobaricInhPa" == grb.typeOfLevel and grb.level in levels:
            if "Temperature" == grb["name"]:
                if idx == 0:
                    TG0.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
                else:
                    TG1.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
            if "Relative humidity" in grb["name"]:
                if idx == 0:
                    TRG0.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
                else:
                    TRG1.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
            if "V component of wind" in grb["name"]:
                if idx == 0:
                    VG0.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
                else:
                    VG1.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
            if "U component of wind" in grb["name"]:
                if idx == 0:
                    UG0.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
                else:
                    UG1.append(merge_grids(Y_speedy_lat, X_speedy_lon, grb))
    grbs.close()

UG0 = np.asarray(UG0)
UG1 = np.asarray(UG1)
VG0 = np.asarray(VG0)
VG1 = np.asarray(VG1)
TG0 = np.asarray(TG0)
TG1 = np.asarray(TG1)
TRG0 = np.asarray(TRG0).reshape((1, 8, 32, 64))
TRG1 = np.asarray(TRG1).reshape((1, 8, 32, 64))
PSG0 = np.asarray(PSG0)
PSG1 = np.asarray(PSG1)

print(f"shape of UG0 {UG0.shape}")
print(f"shape of UG1 {UG1.shape}")
print(f"shape of VG0 {VG0.shape}")
print(f"shape of VG1 {VG1.shape}")
print(f"shape of TG0 {TG0.shape}")
print(f"shape of TG1 {TG1.shape}")
print(f"shape of TRG0 {TRG0.shape}")
print(f"shape of TRG1 {TRG1.shape}")
print(f"shape of PSG0 {PSG0.shape}")
print(f"shape of PSG1 {PSG1.shape}")

##SAVING DATA INTERPOLATED PER LEVEL
np.save("longitude", X_speedy_lon)
np.save("latitude", Y_speedy_lat)
np.save("level", np.asarray(levels))
np.save("UG0", UG0)
np.save("UG1", UG1)
np.save("VG0", VG0)
np.save("VG1", VG1)
np.save("TG0", TG0)
np.save("TG1", TG1)
np.save("TRG0", TRG0)
np.save("TRG1", TRG1)
np.save("PSG0", PSG0)
np.save("PSG1", PSG1)
