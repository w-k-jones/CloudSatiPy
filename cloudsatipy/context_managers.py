"""Context managers for handling hdf file opening/closing/accessing cleanly
"""

from contextlib import contextmanager
from pyhdf import HDF, SD

__all__ = [
    "hdf_manager",
    "vgstart_manager",
    "vgroup_manager",
    "vstart_manager",
    "vdata_manager",
    "sd_manager",
    "sds_manager",
]


def _find_ref_from_name(file, name_or_ref):
    if isinstance(name_or_ref, str):
        ref = file.find(name_or_ref)
    else:
        ref = name_or_ref
    return ref


@contextmanager
def hdf_manager(filename):
    datafile = HDF.HDF(filename)
    try:
        yield datafile
    finally:
        datafile.close()


@contextmanager
def vgstart_manager(datafile):
    v = datafile.vgstart()
    try:
        yield v
    finally:
        v.end()


@contextmanager
def vgroup_manager(v, name_or_ref):
    vg = v.attach(_find_ref_from_name(v, name_or_ref))
    try:
        yield vg
    finally:
        vg.detach()


@contextmanager
def vstart_manager(datafile):
    vs = datafile.vstart()
    try:
        yield vs
    finally:
        vs.end()


@contextmanager
def vdata_manager(vs, name_or_ref):
    vd = vs.attach(_find_ref_from_name(vs, name_or_ref))
    try:
        yield vd
    finally:
        vd.detach()


@contextmanager
def sd_manager(filename):
    sd = SD(filename)
    try:
        yield sd
    finally:
        sd.end()


@contextmanager
def sds_manager(sd, ref):
    sds = sd.select(sd.reftoindex(ref))
    try:
        yield sds
    finally:
        sds.endaccess()
