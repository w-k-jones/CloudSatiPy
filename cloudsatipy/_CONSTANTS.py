"""Constants used by other modules
"""

import numpy as np
from pyhdf.HDF import HC
from pyhdf.SD import SDC

# Map VData types to numpy dtypes
HC_TYPES = {
    HC.CHAR: str,
    HC.CHAR8: str,
    HC.FLOAT32: np.float32,
    HC.FLOAT64: np.float64,
    HC.INT16: np.int16,
    HC.INT32: np.int32,
    HC.INT8: np.int8,
    HC.UCHAR: str,
    HC.UCHAR8: str,
    HC.UINT16: np.uint16,
    HC.UINT32: np.uint32,
    HC.UINT8: np.uint8,
}

# Map Scientific data types to numpy dtypes
SDC_TYPES = {
    SDC.CHAR: str,
    SDC.CHAR8: str,
    SDC.FLOAT32: np.float32,
    SDC.FLOAT64: np.float64,
    SDC.INT16: np.int16,
    SDC.INT32: np.int32,
    SDC.INT8: np.int8,
    SDC.UCHAR: str,
    SDC.UCHAR8: str,
    SDC.UINT16: np.uint16,
    SDC.UINT32: np.uint32,
    SDC.UINT8: np.uint8,
}

# Erroneous fill values
REPLACE_MISSING = {
    "DEM_elevation":-9999,
    "SurfaceClutter_Index":-99,
    "QR":-9999,
    "RH":-999,
    "COD":-99990,
    "Meansolar":-999,
    "Sigmasolar":-999,
    "MeanOSR":-999,
    "SigmaOSR":-999,
    "MeanSSR":-999,
    "SigmaSSR":-999,
    "MeanSFCR":-999,
    "SigmaSFCR":-999,
    "MeanOLR":-999,
    "SigmaOLR":-999,
    "MeanSLR":-999,
    "SigmaSLR":-999,
    "MeanSFCE":-999,
    "SigmaSFCE":-999,
    "MeanQLW":-999,
    "SigmaQLW":-999,
    "MeanQSW":-999,
    "SigmaQSW":-999,
    "CloudFraction":-8,
    "DistanceAvg":-8,
    "dBZe_simulation":-9999,
    "zone":-9999,
    "ze_makeup":-9999,
    "Near_surface_reflectivity":-999,
    "Frozen_precip_height":-999,
    "Freezing_level": -8,
    "SST":-999,

}

REPLACE_MISSOP = {
    "CloudFraction":"<=",
    "DistanceAvg":"<=",
    "EV_1KM_RefSB":"eq",
    "EV_1KM_Emissive":"eq",
    "EV_1KM_Emissive_Uncert_Indexes":"eq",
    "EV_250_RefSB":"eq",
    "EV_500_RefSB":"eq",
}