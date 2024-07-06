"""Constants used by other modules
"""

import numpy as np
from pyhdf.HDF import HC
from pyhdf.SD import SDC

# Map VData types to numpy dtypes
HC_TYPES = {
    HC.CHAR: np.byte,
    HC.CHAR8: np.byte,
    HC.FLOAT32: np.float32,
    HC.FLOAT64: np.float64,
    HC.INT16: np.int16,
    HC.INT32: np.int32,
    HC.INT8: np.int8,
    HC.UCHAR: np.byte,
    HC.UCHAR8: np.byte,
    HC.UINT16: np.uint16,
    HC.UINT32: np.uint32,
    HC.UINT8: np.uint8,
}

# Map Scientific data types to numpy dtypes
SDC_TYPES = {
    SDC.CHAR: np.byte,
    SDC.CHAR8: np.byte,
    SDC.FLOAT32: np.float32,
    SDC.FLOAT64: np.float64,
    SDC.INT16: np.int16,
    SDC.INT32: np.int32,
    SDC.INT8: np.int8,
    SDC.UCHAR: np.byte,
    SDC.UCHAR8: np.byte,
    SDC.UINT16: np.uint16,
    SDC.UINT32: np.uint32,
    SDC.UINT8: np.uint8,
}
