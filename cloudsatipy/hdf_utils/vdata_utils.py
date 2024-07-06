"""Tools for working with hdf VData
"""

import numpy as np
from pyhdf import VS
from pyhdf.HDF import HC

from cloudsatipy.context_managers import vdata_manager
from cloudsatipy._CONSTANTS import HC_TYPES


def vdata_info(vs, ref):
    with vdata_manager(vs, ref) as vd:
        nrecs, intmode, fields, size, name = vd.inquire()
        fieldinfo = vd.fieldinfo()
        fields = {
            fieldname: dict(
                zip(["type", "order", "n_attrs", "index", "external_size"], fi[1:])
            )
            for fieldname, fi in zip(fields, fieldinfo)
        }
        info = {
            "name": name,
            "tag": HC.DFTAG_VH,
            "ref": ref,
            "nrecs": nrecs,
            "intmode": intmode,
            "fields": fields,
            "size": size,
        }
    return info


def get_vdata_array(vs: VS.VS, ref: str | int) -> np.ndarray:
    with vdata_manager(vs, ref) as vd:
        values = read_vdata_array(vd)
    return values


def read_vdata_array(vd: VS.VD) -> np.ndarray:
    vd_type = vd.fieldinfo()[0][1]
    return np.asarray(vd[:], dtype=HC_TYPES[vd_type]).squeeze()
