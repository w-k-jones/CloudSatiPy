import pathlib
import pytest
from cloudsatipy.context_managers import *

test_file = pathlib.Path(
    "/Users/jonesw/python/CloudSatiPy/data/2010195112321_22399_CS_2B-CWC-RVOD_GRANULE_P1_R05_E03_F00.hdf"
)


def test_hdf_manager():
    with hdf_manager(test_file) as hdf:
        _ = hdf.getfileversion()

    # Check that trying to access outside of the context fails
    with pytest.raises(TypeError):
        _ = hdf.close()


def test_vgstart_manager():
    with hdf_manager(test_file) as hdf, vgstart_manager(hdf) as v:
        _ = v.findclass("SWATH")

    # Check that trying to access outside of the context fails
    with pytest.raises(AttributeError):
        _ = v.findclass("SWATH")


def test_vgroup_manager():
    with hdf_manager(test_file) as hdf, vgstart_manager(hdf) as v, vgroup_manager(
        v, v.findclass("SWATH")
    ) as vg:
        _ = vg._name

    # Check that trying to access outside of the context fails
    with pytest.raises(TypeError):
        _ = vg._name


def test_vstart_manager():
    with hdf_manager(test_file) as hdf, vstart_manager(hdf) as vs:
        _ = vs.find("Latitude")

    # Check that trying to access outside of the context fails
    with pytest.raises(AttributeError):
        _ = vs.find("Latitude")


def test_vdata_manager():
    with hdf_manager(test_file) as hdf, vstart_manager(hdf) as vs, vdata_manager(
        vs, vs.find("Latitude")
    ) as vd:
        _ = vd.inquire()

    # Check that trying to access outside of the context fails
    with pytest.raises(TypeError):
        _ = vd.inquire()


def test_sd_manager():
    with sd_manager(test_file) as sd:
        _ = sd.attributes()

    # Check that trying to access outside of the context fails
    with pytest.raises(TypeError):
        _ = sd.attributes()


def test_sds_manager():
    with sd_manager(test_file) as sd, sds_manager(sd, "Height") as sds:
        _ = sds.info()

    # Check that trying to access outside of the context fails
    with pytest.raises(TypeError):
        _ = sds.info()
