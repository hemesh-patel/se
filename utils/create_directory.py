import os


def make_dir(dir_name):
    """
    Create a directory
    :param dir_name: Name of directory
    :return: None
    """
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
    except OSError:
        print('Error: Creating directory.' + dir_name)
