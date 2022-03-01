"""
Contains all image related logic: encoding/decoding, temporary file storage,
and transformations.

Author: Francis Kogge
Date: 02/28/2022
"""

import os
import base64
from PIL import Image


THUMBNAIL_SIZE = (50, 50)


def transform(image_model):
    """
    Transformation pipeline: performs the transformations commands
    requested by the client.
    """
    with Image.open(image_model.filename) as image:
        for command, args in image_model.command_list.items():
            print('command: {}'.format(command))

            if command == 'flipHorizontal':
                image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
            elif command == 'flipVertical':
                image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
            elif command == 'rotate':
                degrees = -int(args)  # PIL rotates counterclockwise
                image = image.rotate(degrees)
            elif command == 'grayscale':
                image = image.convert(mode='L')
            elif command == 'resize':
                width, height = split_resize_args(args)
                image = image.resize((int(width), int(height)))
            elif command == 'thumbnail':
                image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
            elif command == 'rotateLeft':
                image = image.transpose(method=Image.ROTATE_90)
            elif command == 'rotateRight':
                image = image.transpose(method=Image.ROTATE_270)

            image.save('./' + image_model.filename)


def get_image_format(file_storage_obj):
    """
    Returns the image file format.
    :param file_storage_obj: FileStorage object containing the image file
    :return: image file format
    """
    return file_storage_obj.mimetype.split('/')[1]


def get_base64_encoding(image_filename):
    """
    Returns the base64 encoding of the given image file.
    :param image_filename: image file name
    :return: base64 encoded string
    """
    with open(image_filename, 'rb') as f:
        return base64.b64encode(f.read())


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


def split_resize_args(args):
    """
    Splits the arguments provided for the resize command.
    :param args: resize command arguments
    :return: (width, length) pair
    """
    if ',' in args:
        width, height = args.split(',')
    else:
        # If separated by whitespace
        width, height = list(filter(None, args.split(' ')))

    return width.strip(), height.strip()


def invalid_command_list(command_list):
    """
    Performs validation checks on the transformation command list. If it is
    found to be invalid, an appropriate error message is returned.
    :param command_list: transformation command list
    :return: error message if command list is invalid, otherwise None if valid
    """
    for command, args in command_list.items():
        # Any command that is not rotate or resize does not accept any arguments
        if command not in {'rotate', 'resize'} and args:
            return command + ': does not accept parameters'

        # rotate must take a number argument
        elif command == 'rotate' and not args.isnumeric():
            return command + ': invalid value, must be an integer'

        # resize must take a pair of numbers as an argument
        elif command == 'resize':
            try:
                width, height = split_resize_args(args)
            except ValueError:
                return command + ': invalid value, must be a pair of integers separated by a comma or space'
            else:
                if not width.isnumeric() or not height.isnumeric():
                    return command + ': invalid value, must be a pair of integers (width, height)'
    return None
