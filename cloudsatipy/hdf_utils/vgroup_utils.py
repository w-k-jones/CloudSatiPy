"""Tools for working with hdf VGroups
"""

from math import prod
import pandas as pd
from pyhdf import HDF, V, VS, SD
from pyhdf.HDF import HC

from cloudsatipy.context_managers import sds_manager, vdata_manager, vgroup_manager


def vgroup_info(v, ref):
    with vgroup_manager(v, ref) as vg:
        name = vg._name
        info = {"name": name, "tag": HC.DFTAG_VG, "ref": ref, "class": vg._class}
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


def get_vgroup_members_df(v: V.V, vg: V.VG, vs: VS.VS, sd: SD.SD):
    members = vg.tagrefs()
    member_info = []
    for tag, ref in members:
        # Vdata tag
        if tag == HC.DFTAG_VH:
            with vdata_manager(vs, ref) as vd:
                nrecs, _, _, _, name = vd.inquire()
            member_info.append({"name": name, "ref": ref, "tag": tag, "size": nrecs})

        # SDS tag
        elif tag == HC.DFTAG_NDG:
            with sds_manager(sd, ref) as sds:
                name, _, dims, _, _ = sds.info()
            member_info.append(
                {"name": name, "ref": ref, "tag": tag, "size": prod(dims)}
            )

        # VS tag
        elif tag == HC.DFTAG_VG:
            with vgroup_manager(v, ref) as vg0:
                member_info.append(
                    {"name": vg0._name, "ref": ref, "tag": tag, "size": vg0._nmembers}
                )

    return pd.DataFrame(member_info)
