import pathlib
from cloudsatipy import filename_parser


def test_parse_filename():
    test_files = pathlib.Path("/Users/jonesw/python/CloudSatiPy/data/").glob("*.hdf")

    for file in test_files:
        _ = filename_parser.parse_filename(file)
