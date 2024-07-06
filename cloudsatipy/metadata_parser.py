"""Parse global and variable metadata in cloudsat files
"""

import pathlib
from cloudsatipy.context_managers import (
    hdf_manager,
    vgstart_manager,
    vgroup_manager,
    vstart_manager,
    vdata_manager,
)


def get_metadata(filename: str | pathlib.Path) -> tuple[dict, dict]:
    with (
        hdf_manager(filename) as hdf,
        vgstart_manager(hdf) as v,
        vgroup_manager(v, v.find("Swath Attributes")) as vg,
        vstart_manager(hdf) as vs,
    ):
        global_attrs = {}
        variable_attrs = {}
        members = vg.tagrefs()
        for _, ref in members:
            # Vdata tag
            if vg.isvs(ref):
                with vdata_manager(vs, ref) as vd:
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
