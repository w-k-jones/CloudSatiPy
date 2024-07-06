"""Tools for working with hdf VData
"""

from pyhdf.HDF import HC

from cloudsatipy.context_managers import vdata_manager


def vdata_info(vs, ref):
    with vdata_manager(vs, ref) as vd:
        nrecs, intmode, fields, size, name = vd.inquire()
        fieldinfo = vd.fieldinfo()
        fieldinfo = [
            dict(zip(["type", "order", "n_attrs", "index", "external_size"], fi[1:]))
            for fi in fieldinfo
        ]
        fields = dict(zip(fields, fieldinfo))
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
