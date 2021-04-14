import cdsapi
import xarray as xr
import numpy as np

c = cdsapi.Client()

max_wind = 50
wind_resolution = 0.5
bin_count = int(max_wind / wind_resolution)
bins_file_path = './cache/bins.nc'
data_file_path = './tmp/data.nc'

def data_download(date):
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': [
                '100m_u_component_of_wind', '100m_v_component_of_wind',
            ],
            'year': date.year,
            'month': date.month,
            'day': [*range(1, 11)] if date.day == 1 else [*range(11, 21)] if date.day == 11 else [*range(21, 32)], 
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
            # 'area': [60, -10, 35, 30],
            'format': 'netcdf',
        },
        data_file_path
    )

# https://stackoverflow.com/questions/44152436/calculate-histograms-along-axis
def hist_laxis(data, n_bins, range_limits):
    # Setup bins and determine the bin location for each element for the bins
    R = range_limits
    N = data.shape[-1]
    bins = np.linspace(R[0], R[1], n_bins + 1)
    data2D = data.reshape(-1, N)
    idx = np.searchsorted(bins, data2D,'right') - 1

    # Some elements would be off limits, so get a mask for those
    bad_mask = (idx==-1) | (idx==n_bins)

    # We need to use bincount to get bin based counts. To have unique IDs for
    # each row and not get confused by the ones from other rows, we need to 
    # offset each row by a scale (using row length for this).
    scaled_idx = n_bins*np.arange(data2D.shape[0])[:,None] + idx

    # Set the bad ones to be last possible index+1 : n_bins*data2D.shape[0]
    limit = n_bins*data2D.shape[0]
    scaled_idx[bad_mask] = limit

    # Get the counts and reshape to multi-dim
    counts = np.bincount(scaled_idx.ravel(),minlength=limit+1)[:-1]
    counts.shape = data.shape[:-1] + (n_bins,)
    return counts, bins


def update_bins(date, first_build):
    data_download(date)

    print('Load downloaded data')
    data = xr.load_dataset(data_file_path)

    print('Compute wind_speed')
    wind_speed = np.sqrt(data['u100']**2 + data['v100']**2)

    print('Compute bins')
    b, bins = hist_laxis(
        wind_speed.transpose('latitude', 'longitude', 'time').values,
        bin_count,
        (0, max_wind)
    )
    bins_da = xr.DataArray(
        b,
        coords=[
            wind_speed['latitude'].values,
            wind_speed['longitude'].values,
            bins[:-1]
        ],
        dims=["lat", "lng", "bins"]
    )

    if not first_build:
        print('Update bins')
        bins_da = bins_da + xr.load_dataset(bins_file_path)

    print('Write new bins')
    bins_da.to_netcdf(bins_file_path)

def compute_distrib():
    print('Compute distrib')
    pass
