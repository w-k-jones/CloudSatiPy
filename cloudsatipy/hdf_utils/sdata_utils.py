"""Tools for working with hdf scientific data
"""

from pyhdf.HDF import HC

from cloudsatipy.context_managers import sds_manager


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
