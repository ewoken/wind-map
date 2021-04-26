from datetime import date, timedelta
from pathlib import Path


from helpers import read_input, write_build_done, write_result_message, do_exit, write_input
from work import bins_file_path, update_bins, compute_distrib

def get_start_next_month(d):
    return (d.replace(day=1) + timedelta(days=32)).replace(day=1)

start_date = '2000-01-01'
last_date = date.fromisoformat('2020-12-31')

input_string, first_build = read_input(start_date)
input_date = date.fromisoformat(input_string)
print(f'Input date: {input_date}')

if input_date > last_date:
    print('DONE !')
    write_build_done()
    do_exit(0)

if first_build:
    print('First build')
else:
    my_file = Path(bins_file_path)
    if not my_file.is_file():
        raise ValueError(f'{bins_file_path} should be present')

print('Start work')

update_bins(input_date, first_build)

if input_date == last_date:
    compute_distrib()

next_date = input_date + timedelta(days=10) if input_date.day != 21 else get_start_next_month(input_date)
print(f'Next input {next_date}')
write_input(str(next_date))

message = f'Done {input_date}'
print(message)
write_result_message(message)