import pathlib
from typing import Optional

import xarray as xr

from cloudsatipy.reader import CloudsatReader


def open_cloudsat(
    filename: str | pathlib.Path,
    variable: Optional[str | list] = None,
    standardise_dims: bool = True,
) -> xr.Dataset:
    """Read cloudsat HDF files into an xarray dataset

    Parameters
    ----------
    filename : str | pathlib.Path
        Path to file as string or pathlib
    variable : Optional[str  |  list]
        Variable or list of variables to read, default None. If None, all
        variables will be read
    standardise_dims : bool
        If True, all dimensions will be changed to standardised naming e.g.
        "Nray", "Nbin", default True

    Returns
    -------
    xr.Dataset
        xarray dataset containing requested data
    """
    reader = CloudsatReader(filename)
    reader.read_data(variable)
    if standardise_dims:
        reader.standardise_dims()
    return reader.data
