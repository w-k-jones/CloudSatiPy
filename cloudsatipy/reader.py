"""Reader for cloudsat files
"""

import pathlib
from typing import Optional

import xarray as xr
from pyhdf.HDF import HC

from cloudsatipy.context_managers import *
from cloudsatipy.data_processing import mask_and_scale_da
from cloudsatipy.filename_parser import parse_filename
from cloudsatipy.hdf_utils.sdata_utils import get_sdata_dataarray
from cloudsatipy.hdf_utils.vdata_utils import get_vdata_array
from cloudsatipy.hdf_utils.vgroup_utils import get_vgroup_info_df, get_vgroup_members_df
from cloudsatipy.metadata_parser import get_metadata


class CloudsatReader:
    def __init__(self, filename: str | pathlib.Path) -> None:
        self.data = xr.Dataset()
        self.file_info = parse_filename(filename)
        with (
            hdf_manager(self.file_info.filename) as self.hdf,
            vgstart_manager(self.hdf) as self.v,
            vstart_manager(self.hdf) as self.vs,
            sd_manager(self.file_info.filename) as self.sd,
        ):
            self._get_vgroup_info_df()
            self._check_vgroup_info()
            self._get_metadata()
            self._get_geolocation_info()
            self._get_data_info()
            self._get_dimensions()
            self._read_geolocation_data()

    def _get_vgroup_info_df(self):
        self.vgroup_info = get_vgroup_info_df(self.v)

    def _check_vgroup_info(self):
        gb_class = self.vgroup_info.groupby("class")
        assert (
            len(gb_class.get_group("SWATH")) == 1
        ), f'Wrong number of SWATH detected; expected 1, found {len(gb_class.get_group("SWATH"))}'
        assert (
            gb_class.get_group("SWATH")["name"].item() == self.file_info.product
        ), f'Wrong name of SWATH; expected {self.file_info.product}, found{gb_class.get_group("SWATH")["name"].item()}'
        assert (
            len(gb_class.get_group("SWATH Vgroup")) == 3
        ), f'Wrong number of SWATH VGroups detected; expected 3, found {len(gb_class.get_group("SWATH Vgroup"))}'
        for name in ["Geolocation Fields", "Data Fields", "Swath Attributes"]:
            assert (
                name in gb_class.get_group("SWATH Vgroup")["name"].to_list()
            ), f"Missing SWATH VGroup name; {name}"

    def _get_metadata(self):
        with vgroup_manager(
            self.v, self.v.find("Swath Attributes")
        ) as swath_attributes_vgroup:
            self.global_attrs, self.variable_attrs = get_metadata(
                swath_attributes_vgroup, self.vs
            )
        self.data = self.data.assign_attrs(self.global_attrs)

    def _get_geolocation_info(self):
        with vgroup_manager(
            self.v, self.v.find("Geolocation Fields")
        ) as geolocation_vgroup:
            self.geolocation_info = get_vgroup_members_df(
                self.v, geolocation_vgroup, self.vs, self.sd
            ).set_index("name")

    def _get_data_info(self):
        with vgroup_manager(self.v, self.v.find("Data Fields")) as data_vgroup:
            self.data_info = get_vgroup_members_df(
                self.v, data_vgroup, self.vs, self.sd
            ).set_index("name")

    def _get_dimensions(self):
        self.dimensions = {}

        dimension_vgroups = self.vgroup_info.groupby("class").get_group("Dim0.0")

        for _, dimension in dimension_vgroups.iterrows():
            with vgroup_manager(self.v, dimension["ref"]) as vg:
                vdata_ref = vg.tagref(0)[1]
                self.dimensions[dimension["name"]] = get_vdata_array(
                    self.vs, vdata_ref
                ).item()

        for sds_info in self.sd.datasets().values():
            for dim_name, dim_size in zip(sds_info[0], sds_info[1]):
                if dim_name not in self.dimensions:
                    self.dimensions = dim_size

        if self.geolocation_info.loc["Profile_time"]["size"] not in self.dimensions.values():
            self.dimensions["Nray"] = int(self.geolocation_info.loc["Profile_time"]["size"])


        self._inverse_dimensions = dict(
            zip(self.dimensions.values(), self.dimensions.keys())
        )

    def _read_a_var(self, name, ref, tag):
        if tag == HC.DFTAG_VH:  # is Vdata:
            variable = get_vdata_array(self.vs, ref)
            if variable.size > 1:
                da = xr.DataArray(
                    variable, dims=self._inverse_dimensions[variable.size], name=name
                )
            else:
                da = xr.DataArray(variable.item(), name=name)

        elif tag == HC.DFTAG_NDG:  # is scientific data
            da = get_sdata_dataarray(self.sd, ref)

        if name in self.variable_attrs:
            da = da.assign_attrs(self.variable_attrs[name])
            da = mask_and_scale_da(da)

        return da

    def _read_geolocation_data(self):
        for name, row in self.geolocation_info.iterrows():
            self.data[name] = self._read_a_var(name, row["ref"], row["tag"])
        self.data = self.data.set_coords(self.geolocation_info.index)

    def read_data(self, variable: Optional[str | list[str]] = None):
        """Read scientific data from the Cloudsat file into the dataset

        Parameters
        ----------
        variable : Optional[str  |  list[str]], optional
            variable names; a single name, a list of names, by default None. If
            None is provided, all variables will be read
        """
        with (
            hdf_manager(self.file_info.filename) as self.hdf,
            vgstart_manager(self.hdf) as self.v,
            vstart_manager(self.hdf) as self.vs,
            sd_manager(self.file_info.filename) as self.sd,
        ):
            if variable is None:
                variable = self.data_info.index
            elif isinstance(variable, str):
                variable = [variable]

            for varname, row in self.data_info.loc[variable].iterrows():
                self.data[varname] = self._read_a_var(varname, row["ref"], row["tag"])

    def standardise_dims(self):
        """Change dims to a standard format, rather than the different dim names 
        provided with different cloudsat files 
        """
        dim_mapping = {dim:dim.split(":")[0].lower().title() for dim in self.data.dims}
        self.data = self.data.swap_dims(dim_mapping)
