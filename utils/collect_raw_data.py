import requests
import os


def collect_data(url, dir_name, file_name):
    """
    Function collects data from a given url and puts the data into the 'raw_data' directory

    :param url: url of where data is stored
    :param dir_name: name of directory where data will be stored
    :param file_name: name of file where data is to be stored

    :return: None
    """
    dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), dir_name)  # We go 2 levels above
    full_path = os.path.join(dir_path, file_name)

    response = requests.get(url)

    with open(full_path, 'wb') as file:
        file.write(response.content)

