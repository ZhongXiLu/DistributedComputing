# https://stackoverflow.com/a/39110

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove
import sys


def replace(file_path, new_ip):

    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if 'PROXY_URL' in line:
                    new_file.write(f'    url: \'{new_ip}\'  // PROXY_URL\n')
                else:
                    new_file.write(line)

    # Remove original file
    remove(file_path)

    # Move new file
    move(abs_path, file_path)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        replace('src/environments/environment.ts', sys.argv[1])
