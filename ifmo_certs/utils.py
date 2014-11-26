import os
import errno


def get_file_contents(filename):
    with open(filename, "r") as f:
        return f.read()


def ensure_dir(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise