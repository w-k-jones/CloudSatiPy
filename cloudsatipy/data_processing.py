"""Process data provided by Cloudsat files
"""

from datetime import datetime
import numpy as np
import pandas as pd
import xarray as xr


def mask_and_scale_da(da: xr.DataArray, fill_value=np.nan) -> xr.DataArray:
    if "missing" in da.attrs and "missop" in da.attrs:
        da = filter_missing_values(da, da.missing, da.missop, fill_value=fill_value)
    if "factor" in da.attrs and "offset" in da.attrs:
        da = apply_scale_and_offset(da, da.factor, da.offset)
    return da


def filter_missing_values(
    da: xr.DataArray, missing_value: float, missop: str, fill_value: float = np.nan
) -> xr.DataArray:
    "<, <=, ==, >=, or >"
    if missop == "==" or missop == "eq":
        wh_valid = da != np.float32(missing_value)
    elif missop == "<" or missop == "lt":
        wh_valid = da >= np.float32(missing_value)
    elif missop == "<=" or missop == "le":
        wh_valid = da > np.float32(missing_value)
    elif missop == ">=" or missop == "ge":
        wh_valid = da < np.float32(missing_value)
    elif missop == ">" or missop == "gt":
        wh_valid = da <= np.float32(missing_value)
    else:
        raise ValueError(f"Missop {missop} is not valid")
    return da.where(wh_valid, other=np.float32(fill_value))


def apply_scale_and_offset(
    da: xr.DataArray, factor: float, offset: float
) -> xr.DataArray:
    """Apply scale and offset to Cloudsat data. This is applied the opposite way
    to standard...

    Parameters
    ----------
    da : xr.DataArray
        _description_
    factor : float
        _description_
    offset : float
        _description_

    Returns
    -------
    xr.DataArray
        _description_
    """
    da.data = (da.data - np.float32(offset)) / np.float32(factor)
    return da


def process_cloudsat_times(
    profile_time_seconds: xr.DataArray,
    utc_offset: xr.DataArray,
    file_timestamp: datetime,
) -> xr.DataArray:
    start_time = np.datetime64(
        file_timestamp.strftime("%Y-%m-%dT00:00:00")
    ) + np.timedelta64(int(utc_offset.item() * 1e9), "ns")
    profile_times = pd.DatetimeIndex(
        start_time + (profile_time_seconds.data * 1e9).astype("timedelta64[ns]")
    )
    return profile_time_seconds.copy(data=profile_times)
