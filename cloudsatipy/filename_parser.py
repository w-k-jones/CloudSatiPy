"""Utils for handling cloudsat filenames
"""

import pathlib
from datetime import datetime
from dataclasses import dataclass


@dataclass
class CloudsatFileInfo:
    filename: str
    start_date: datetime
    granule_number: int
    product: str
    processing_iteration: str
    release: str
    epoch: str
    fix: str


def parse_filename(filename: str | pathlib.Path) -> CloudsatFileInfo:
    if isinstance(filename, str):
        filename = pathlib.Path(filename)

    assert filename.exists, f"File {filename} does not exist"
    (
        start_date,
        granule_number,
        _,
        product,
        _,
        processing_iteration,
        release,
        epoch,
        fix,
    ) = filename.stem.split("_")
    start_date = datetime.strptime(start_date, "%Y%j%H%M%S")
    return CloudsatFileInfo(
        str(filename),
        start_date,
        granule_number,
        product,
        processing_iteration,
        release,
        epoch,
        fix,
    )
