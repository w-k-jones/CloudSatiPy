import pathlib

from cloudsatipy.reader import CloudsatReader

test_file = pathlib.Path(
    "/Users/jonesw/python/CloudSatiPy/data/2010195112321_22399_CS_2B-CWC-RVOD_GRANULE_P1_R05_E03_F00.hdf"
)


def test_init_cloudsatreader():
    test_files = pathlib.Path("/Users/jonesw/python/CloudSatiPy/data/").glob("*.hdf")

    for file in test_files:
        reader = CloudsatReader(file)
        reader.read_data()
