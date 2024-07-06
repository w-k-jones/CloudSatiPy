"""Tools for working with hdf scientific data
"""

import numpy as np
import xarray as xr
from pyhdf import SD
from pyhdf.HDF import HC
from pyhdf.SD import SDC

from cloudsatipy.context_managers import sds_manager
from cloudsatipy._CONSTANTS import SDC_TYPES


def sd_info(sd, ref):
    with sds_manager(sd, ref) as sds:
        name, rank, shape, sdc_type, nattrs = sds.info()
        info = {
            "name": name,
            "tag": HC.DFTAG_NDG,
            "ref": ref,
            "rank": rank,
            "shape": shape,
            "type": sdc_type,
            "n_attrs": nattrs,
            "dimensions": sds.dimensions(),
        }
    return info


def get_sdata_dataarray(sd: SD.SD, ref: str | int) -> xr.DataArray:
    with sds_manager(sd, ref) as sds:
        da = read_sdata_dataarray(sds)
    return da


def read_sdata_dataarray(sds: SD.SDS) -> np.ndarray:
    name, _, _, sds_type, _ = sds.info()
    dims = sds.dimensions()
    data = np.asarray(sds[:], dtype=SDC_TYPES[sds_type])
    return xr.DataArray(data, dims=dims, name=name, attrs=sds.attributes())
