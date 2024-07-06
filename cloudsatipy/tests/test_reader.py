import pathlib

import numpy as np

from cloudsatipy.reader import CloudsatReader

def test_init_cloudsatreader():
    test_files = pathlib.Path("/Users/jonesw/python/CloudSatiPy/data/").glob("*.hdf")

    for test_file in test_files:
        reader = CloudsatReader(test_file)
        reader.read_data()
        assert np.issubdtype(reader.data.Profile_time.dtype, np.datetime64), "Profile time not converted to datetimes correctly"
