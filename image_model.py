"""
Data model for an image which consists of the image filename and the list of
transformation commands.

Author: Francis Kogge
Date: 02/28/2022
"""

from PIL import Image

THUMBNAIL_SIZE = (50, 50)


class ImageModel(object):
    def __init__(self, image_filename, command_list):
        """
        Initializes the image model.
        :param image_filename: name of image file
        :param command_list: list of transformation commands
        """
        self.filename = image_filename
        self.command_list = command_list

    def transform(self):
        """
        Transformation pipeline: performs the transformations commands
        requested by the client.
        """
        with Image.open(self.filename) as image:
            for command, args in self.command_list.items():
                print('command: {}({})'.format(command, args if args else ''))

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
                    size = self.split_resize_args(args)  # (width, height) pair
                    image = image.resize(size)
                elif command == 'thumbnail':
                    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
                elif command == 'rotateLeft':
                    image = image.transpose(method=Image.ROTATE_90)
                elif command == 'rotateRight':
                    image = image.transpose(method=Image.ROTATE_270)

                image.save('./' + self.filename)

    @staticmethod
    def split_resize_args(args):
        """
        Splits the arguments provided for the resize command.
        :param args: resize command arguments
        :return: (width, length) pair
        """
        if ',' in args:
            width, height = args.split(',')
        else:  # If separated by whitespace
            width, height = list(filter(None, args.split(' ')))

        return int(width.strip()), int(height.strip())
