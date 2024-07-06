import pathlib
import pytest
from cloudsatipy.context_managers import *
from cloudsatipy.metadata_parser import get_metadata

test_file = pathlib.Path(
    "/Users/jonesw/python/CloudSatiPy/data/2010195112321_22399_CS_2B-CWC-RVOD_GRANULE_P1_R05_E03_F00.hdf"
)


def test_get_metadata():
    with (
        hdf_manager(test_file) as hdf,
        vgstart_manager(hdf) as v,
        vgroup_manager(v, v.find("Swath Attributes")) as swath_attributes_vgroup,
        vstart_manager(hdf) as vstart,
    ):
        _ = get_metadata(swath_attributes_vgroup, vstart)
