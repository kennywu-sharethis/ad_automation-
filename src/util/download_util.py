import time
import os
from datetime import datetime
import pytz

def download_wait(directory, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.
    """
    dl_wait = True
    while dl_wait:
        time.sleep(2)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.part'):
                dl_wait = True
    return True

def num_files(directory: str):
    """
    :param directory:
        directory folder path of location of files
    :return:
        number of files in specified directory
    """
    return len(os.listdir(directory))

def verify_file_size(file_path: str, threshold):
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        if size < threshold:
            return False
        else:
            return True
    else:
        return False

def remove_file(file_path: str):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error removing file '{file_path}': {e}")


def get_publicwww_filename(directory:str):
    latest_file = None
    latest_timestamp = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_timestamp = os.path.getmtime(file_path)
            if file_timestamp > latest_timestamp:
                latest_timestamp = file_timestamp
                latest_file = filename
    return latest_file