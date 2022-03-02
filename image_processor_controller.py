"""
API controller that provides the client-accessible endpoint which can be called
in order to transform the client-provided image.

Author: Francis Kogge
02/28/2022
"""

import file_service
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from image_model import ImageModel

VALID_IMAGE_FORMATS = {'png', 'jpeg', 'jpg', 'tiff', 'gif'}

app = Flask(__name__)
cors = CORS(app)


@app.route('/transform', methods=['POST'])
def get_transformed_image():
    """
    API endpoint that transforms the client-supplied image (must be in a valid
    format). The image and transformation commands are supplied in the request
    body. Sends back an HTML page to render the image encoded in base-64.
    :return: HTTP response
             - HTML page with base-64 encoded image, 200 (success)
             - Error message, 400 (missing image, invalid image format, or
               missing transformation commands
    """
    # Validate file is in the request body
    if not request.files:
        return jsonify({'Error': 'no image file provided'}), 400

    # Validate transformation command list is in request body form data
    if not request.form:
        return jsonify({'Error': 'no transformation command provided'}), 400
    file_storage_obj = request.files['imageFile']

    # Validate image file format is valid
    image_format = file_service.get_image_file_format(file_storage_obj)
    if image_format not in VALID_IMAGE_FORMATS:
        return jsonify('Invalid image format, must be one of {}'
                       .format(list(VALID_IMAGE_FORMATS))), 400

    # Validate command parameter values, or lack thereof
    command_list = dict(request.form)
    error_msg = invalid_command_list(command_list)
    if error_msg:
        return jsonify({'Error': error_msg}), 400

    # Create temporary image and perform transformations on it
    filename = 'temp_image.{}'.format(image_format)
    file_service.create_temp_image(file_storage_obj, filename)
    ImageModel(filename, command_list).transform()

    # Store image file data in memory then delete it
    file_data = file_service.get_file_data(filename)
    file_service.delete_temp_image(filename)

    return send_file(file_data, mimetype='image/{}'.format(image_format))


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
                ImageModel.split_resize_args(args)
            except ValueError:
                return command + ': invalid value, must be a pair of integers ' \
                                 'separated by a comma or space (width, height)'

    return None

if __name__ == '__main__':
    app.run(debug=True, port=55321)
