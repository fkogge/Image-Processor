def image_render_html(b64_img_str):
    return '''<div><p>Transformed Image</p>
        <img src="data:image/jpeg;base64, {}\"></div>
        '''.format(b64_img_str.decode())