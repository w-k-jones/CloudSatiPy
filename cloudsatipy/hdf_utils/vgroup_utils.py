"""Tools for working with hdf VGroups
"""

import pandas as pd
from pyhdf import HDF, V
from pyhdf.HDF import HC

from cloudsatipy.context_managers import vgroup_manager


def vgroup_info(v, ref):
    with vgroup_manager(v, ref) as vg0:
        name = vg0._name
        info = {"name": name, "tag": HC.DFTAG_VG, "ref": ref, "class": vg0._class}
    return info


def get_vgroup_info_df(v: V.V):
    ref = -1
    vgroup_info_list = []
    while 1:
        try:
            ref = v.getid(ref)
            vgroup_info_list.append(vgroup_info(v, ref))
        except HDF.HDF4Error:  # no more vgroup
            break
    return pd.DataFrame(vgroup_info_list)
