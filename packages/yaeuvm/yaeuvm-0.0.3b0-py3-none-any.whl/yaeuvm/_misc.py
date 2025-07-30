import functools
import xarray as xr
from importlib_resources import files


@functools.cache
def _read_coeffs(file):
    return xr.open_dataset(files('yaeuvm._coeffs').joinpath(file))

def get_yaeuvm_ba():
    return _read_coeffs('_yaeuvm_ba_coeffs.nc').copy()

def get_yaeuvm_r():
    return _read_coeffs('_yaeuvm_r_coeffs.nc').copy()

def get_yaeuvm_br():
    return _read_coeffs('_yaeuvm_br_coeffs.nc').copy()
