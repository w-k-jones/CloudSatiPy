import numpy as np
import xarray as xr

def construct_cloud_type_mask(cldclass_ds):
    """Convert the layer properties from cloudsat cldclass-lidar files into 
    cloud type masks

    Parameters
    ----------
    cldclass_ds : xr.Dataset
        Cloudsat 2B cldclass-lidar dataset, including the variables Height, 
        CloudLayerTop, CloudLayerBase, CloudLayerType and CloudTypeQuality

    Returns
    -------
    cloud_type_mask : xr.DataArray
        Dataarray of shape (Nray, Nbins) of cloud type for each Cloudsat height
        bin

    cloud_type_quality : xr.DataArray
        The quality flag associated with the cloud type 
    """
    cloud_type_mask = xr.DataArray(
        np.zeros_like(cldclass_ds.Height.values), cldclass_ds.Height.coords, cldclass_ds.Height.dims
    )
    cloud_type_quality = xr.DataArray(
        np.zeros_like(cldclass_ds.Height.values), cldclass_ds.Height.coords, cldclass_ds.Height.dims
    )

    for cloud_layer in cldclass_ds.Ncloud.values:
        if np.any(cldclass_ds.CloudLayerType[cloud_layer]).item():
            raveled_idx, n_cloud_bins = _get_layer_indices(
                cldclass_ds.Height, 
                cldclass_ds.CloudLayerTop[...,cloud_layer], 
                cldclass_ds.CloudLayerBase[...,cloud_layer], 
            )
            cloud_type_mask.data.ravel()[raveled_idx] = np.repeat(
                cldclass_ds.CloudLayerType[...,cloud_layer].values, n_cloud_bins
            )
            cloud_type_quality.data.ravel()[raveled_idx] = np.repeat(
                cldclass_ds.CloudTypeQuality[...,cloud_layer].values, n_cloud_bins
            )
        else:
            break

    attrs = cldclass_ds.CloudLayerType.attrs.copy()

    attrs["Flag_values"] = ["Deep", "Ns", "Cu", "Sc", "St", "Ac", "As", "High"][::-1]

    cloud_type_mask = cloud_type_mask.assign_attrs(attrs)

    quality_attrs = cldclass_ds.CloudTypeQuality.attrs.copy()
    
    cloud_type_quality = cloud_type_quality.assign_attrs(quality_attrs)
    cloud_type_quality[...,0] = 0
    
    return cloud_type_mask, cloud_type_quality


def _find_nearest_height_bins(heights, layer_height):
    return np.nanargmin(
        np.abs(heights - (layer_height.fillna(np.inf)*1e3)).values, axis=1
    )

def _get_layer_indices(heights, layer_top, layer_base):
    top_bin = _find_nearest_height_bins(heights, layer_top)
    base_bin = _find_nearest_height_bins(heights, layer_base)
    
    n_cloud_bins = base_bin - top_bin + 1

    nbin_idx = np.repeat(top_bin, n_cloud_bins) + _repeat_ranges(n_cloud_bins)
    nray_idx = np.repeat(heights.Nray.values, n_cloud_bins)

    raveled_idx = np.ravel_multi_index([nray_idx.astype(int), nbin_idx.astype(int)], heights.shape)
    
    return raveled_idx, n_cloud_bins

def _repeat_ranges(n_repeats):
    repeat_range = np.repeat(np.ones(n_repeats.size), n_repeats)
    repeat_range[np.cumsum(n_repeats)[:-1]] = -n_repeats[:-1]+1
    repeat_range = np.cumsum(repeat_range)-1
    return repeat_range