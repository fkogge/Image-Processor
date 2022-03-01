"""
Data model for an image which consists of the image filename and the list of
transformation commands.

Author: Francis Kogge
Date: 02/28/2022
"""


class ImageModel(object):
    def __init__(self, image_filename, command_list):
        """
        Initializes the image model.
        :param image_filename: name of image file
        :param command_list: list of transformation commands
        """
        self.filename = image_filename
        self.command_list = command_list
