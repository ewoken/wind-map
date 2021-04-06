from pathlib import Path
import sys 

input_path = './outputs/input.txt'

def read_input(default):
    my_file = Path(input_path)
    if my_file.is_file():
        with open(input_path, 'r') as f:
            return f.read()
    else:
        return default

def write_input(data):
    with open(input_path, 'w') as f:
        f.write(data)

def write_build_done():
    with open('./tmp/BUILD_DONE.txt', 'w') as f:
        f.write('1')

def write_result_message(message):
    with open('./tmp/RESULT_MESSAGE.txt', 'w') as f:
        f.write(message)

def do_exit(code):
    sys.exit(code)
