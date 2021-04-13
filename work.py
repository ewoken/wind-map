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
            'day': date.day,
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

def update_bins(date, first_build):
    data_download(date)

    print('Load downloaded data')
    data = xr.load_dataset(data_file_path)

    print('Compute wind_speed')
    wind_speed = np.sqrt(data['u100']**2 + data['v100']**2)

    lats = wind_speed['latitude'].values
    lngs = wind_speed['longitude'].values
    bins = np.histogram(wind_speed.sel(latitude=42, longitude=5), range=(0, max_wind), bins=bin_count)[1][:-1]

    def gen(lat):
        print(f'Compute bins for latitude: {lat}')
        return np.array([
            np.histogram(wind_speed.sel(latitude=lat, longitude=lng), range=(0, max_wind), bins=bin_count)[0]
            for lng in lngs
        ])

    print('Compute bins')
    data_bins = np.array([
        gen(lat)
        for lat in lats
    ])
    bins_da = xr.DataArray(data_bins, coords=[lats, lngs, bins], dims=["lat", "lng", "bins"])

    if not first_build:
        print('Update bins')
        bins_da = bins_da + xr.load_dataset(bins_file_path)

    print('Write new bins')
    bins_da.to_netcdf(bins_file_path)

def compute_distrib():
    print('Compute distrib')
    pass