"""
API controller that provides the client-accessible endpoint which can be called
in order to transform the client-provided image.

Author: Francis Kogge
02/28/2022
"""

import views
import image_service
from flask import Flask, request, jsonify
from flask_cors import CORS
from image_model import ImageModel

VALID_IMAGE_FORMATS = {'png', 'jpeg', 'jpg', 'gif'}

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
        return jsonify('Error: no image file provided'), 400

    # Validate transformation command list is in request body form data
    if not request.form:
        return jsonify('Error: no transformation command provided'), 400
    file_storage_obj = request.files['base64ImageString']

    # Validate image file format is valid
    image_format = image_service.get_image_format(file_storage_obj)
    if image_format not in VALID_IMAGE_FORMATS:
        return jsonify('Invalid image format, must be one of {}'
                       .format(list(VALID_IMAGE_FORMATS))), 400

    # Validate command parameter values, or lack thereof
    command_list = dict(request.form)
    error_msg = image_service.invalid_command_list(command_list)
    if error_msg:
        return error_msg, 400

    # Create temporary image and perform transformations on it
    image_filename = 'temp_image.{}'.format(image_format)
    image_service.create_temp_image(file_storage_obj, image_filename)
    image_model = ImageModel(image_filename, command_list)
    image_service.transform(image_model)
    b64_img_str = image_service.get_base64_encoding(image_filename)
    image_service.delete_temp_image(image_filename)

    return views.image_render_html(b64_img_str), 200


if __name__ == '__main__':
    app.run(debug=True, port=55321)
