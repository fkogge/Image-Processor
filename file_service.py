"""
Contains all file related operations: retrieving file format, creating/deleting
file, and store file data to memory.

Author: Francis Kogge
Date: 02/28/2022
"""

import os
from io import BytesIO


def get_image_file_format(file_storage_obj):
    """
    Returns the image file format.
    :param file_storage_obj: FileStorage object containing the image file
    :return: image file format
    """
    return file_storage_obj.mimetype.split('/')[1]


def create_temp_image(file_storage_obj, filename):
    """
    Creates a temporary image file in the current directory.
    :param file_storage_obj: FileStorage object containing the image file
    :param filename: name of image file
    """
    with open(filename, 'wb') as f:
        file_storage_obj.save(f)
        print('saved temporary image to {}'.format(filename))


def delete_temp_image(filename):
    """
    Removes the given file from the current directory.
    :param filename: name of the file
    """
    os.remove(filename)
    print('deleted temporary image: {}'.format(filename))


def get_file_data(filename):
    """
    Stores the file data in memory and returns the file data.
    :param filename: name of file to store
    :return: file data stored in memory
    """
    file_data = BytesIO()
    with open(filename, 'rb') as f:
        file_data.write(f.read())
    file_data.seek(0)  # Move to first byte
    return file_data
