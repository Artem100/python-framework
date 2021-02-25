import json

from conftest import LOGGER


def read_file(file_path):
    LOGGER.info("Read data from file: '{}'".format(file_path))
    with open(file_path) as f:
        data = json.loads(f.read())
    return data