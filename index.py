import xarray as xr
import numpy as np
from datetime import date, timedelta

from data_download import data_download
from helpers import read_input, write_build_done, write_result_message, do_exit, write_input

last_year = 2020
max_wind = 100
wind_resolution = 0.1
bins = max_wind / wind_resolution

input_date = date.fromisoformat(read_input('2000-01-01'))
print(f'Input date: {input_date}')

if input_date.year > last_year:
    print('DONE !')
    write_build_done()
    do_exit(0)

print('Start download')
# data_download('2000', '01', '01')

# data = xr.load_dataset('./tmp/data.nc')
# wind_speed = np.sqrt(data['u100']**2 + data['v100']**2)

# lats = wind_speed['latitude'].values # [0, 0.25, 0.5]
# lngs = wind_speed['longitude'].values # [1, 1.25, 1.5]
# edges = np.histogram(wind_speed.sel(latitude=0, longitude=0), range=(0, max_wind), bins=bins)[1][:-1]

# def gen(lat):
#     print(lat)
#     return np.array([
#         np.histogram(wind_speed.sel(latitude=lat, longitude=lng), range=(0, max_wind), bins=bins)[0]
#         for lng in lngs
#     ])

# new_data = np.array([
#     gen(lat)
#     for lat in lats
# ])
# new_da = xr.DataArray(new_data, coords=[lats, lngs, edges], dims=["lat", "lng", "edges"])

# new_da.to_netcdf("test.nc")

next_date = input_date + timedelta(days=1)
print(f'Next input {next_date}')
write_input(str(next_date))

write_result_message(f'Done {input_date}')