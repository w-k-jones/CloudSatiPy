"""Context managers for handling hdf file opening/closing/accessing cleanly
"""

from contextlib import contextmanager
import pathlib
from pyhdf import HDF, VS, V, SD

__all__ = [
    "hdf_manager",
    "vgstart_manager",
    "vgroup_manager",
    "vstart_manager",
    "vdata_manager",
    "sd_manager",
    "sds_manager",
]


def _check_if_pathlib(filename: str | pathlib.Path) -> str:
    if isinstance(filename, pathlib.Path) or issubclass(type(filename), pathlib.Path):
        file_str = str(filename)
    else:
        file_str = filename
    return file_str


def _find_ref_from_name(vdata_or_vgroup: VS.VS | V.V, name_or_ref: str | int) -> int:
    if isinstance(name_or_ref, str):
        ref = vdata_or_vgroup.find(name_or_ref)
    else:
        ref = name_or_ref
    return ref


@contextmanager
def hdf_manager(filename: str | pathlib.Path) -> HDF.HDF:
    datafile = HDF.HDF(_check_if_pathlib(filename))
    try:
        yield datafile
    finally:
        datafile.close()


@contextmanager
def vgstart_manager(datafile: HDF.HDF) -> V.V:
    v = datafile.vgstart()
    try:
        yield v
    finally:
        v.end()


@contextmanager
def vgroup_manager(v: V.V, name_or_ref: str | int) -> V.VG:
    vg = v.attach(_find_ref_from_name(v, name_or_ref))
    try:
        yield vg
    finally:
        vg.detach()


@contextmanager
def vstart_manager(datafile: HDF.HDF) -> VS.VS:
    vs = datafile.vstart()
    try:
        yield vs
    finally:
        vs.end()


@contextmanager
def vdata_manager(vs: VS.VS, name_or_ref: str | int) -> VS.VD:
    vd = vs.attach(_find_ref_from_name(vs, name_or_ref))
    try:
        yield vd
    finally:
        vd.detach()


@contextmanager
def sd_manager(filename: str | pathlib.Path) -> SD.SD:
    sd = SD.SD(_check_if_pathlib(filename))
    try:
        yield sd
    finally:
        sd.end()


@contextmanager
def sds_manager(sd: SD.SD, ref: int) -> SD.SDS:
    sds = sd.select(sd.reftoindex(ref))
    try:
        yield sds
    finally:
        sds.endaccess()
