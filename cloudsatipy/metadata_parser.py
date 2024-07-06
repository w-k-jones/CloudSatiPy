"""Parse global and variable metadata in cloudsat files
"""

from pyhdf import V, VS
from cloudsatipy.context_managers import vdata_manager
from cloudsatipy.hdf_utils.vdata_utils import read_vdata_array


def get_metadata(swath_attributes_vgroup: V.VG, vstart: VS.VS) -> tuple[dict, dict]:
    global_attrs = {}
    variable_attrs = {}
    members = swath_attributes_vgroup.tagrefs()
    for _, ref in members:
        if swath_attributes_vgroup.isvs(ref):
            with vdata_manager(vstart, ref) as vd:
                _, _, _, _, name = vd.inquire()
                variable = read_vdata_array(vd)
                if variable.size == 1:
                    variable = variable.item()
                else:
                    variable = variable.tolist()

            if name.startswith("_FV_"):
                varname = name[4:]
                if varname not in variable_attrs:
                    variable_attrs[varname] = {"_FillValue": variable}
                else:
                    variable_attrs[varname]["_FillValue"] = variable
            elif "." in name:
                varname, attrname = name.split(".")
                # Check unit attrs as sometimes a single character can be concerted to a int value
                if attrname == "units":
                    try:
                        variable = chr(int(variable))
                    except ValueError:
                        pass
                if varname not in variable_attrs:
                    variable_attrs[varname] = {attrname: variable}
                else:
                    variable_attrs[varname][attrname] = variable
            else:
                global_attrs[name] = variable

    return global_attrs, variable_attrs
