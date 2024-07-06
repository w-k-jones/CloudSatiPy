"""Parse global and variable metadata in cloudsat files
"""

from pyhdf import V, VS
from cloudsatipy.context_managers import vdata_manager


def get_metadata(swath_attributes_vgroup: V.VG, vstart: VS.VS) -> tuple[dict, dict]:
    global_attrs = {}
    variable_attrs = {}
    members = swath_attributes_vgroup.tagrefs()
    for _, ref in members:
        if swath_attributes_vgroup.isvs(ref):
            with vdata_manager(vstart, ref) as vd:
                length, _, _, _, name = vd.inquire()
                variable = vd.read(length)[0][0]
            if name.startswith("_FV_"):
                varname = name[4:]
                if varname not in variable_attrs:
                    variable_attrs[varname] = {"_FillValue": variable}
                else:
                    variable_attrs[varname]["_FillValue"] = variable
            elif "." in name:
                varname, attrname = name.split(".")
                if varname not in variable_attrs:
                    variable_attrs[varname] = {attrname: variable}
                else:
                    variable_attrs[varname][attrname] = variable
            else:
                global_attrs[name] = variable

    return global_attrs, variable_attrs
