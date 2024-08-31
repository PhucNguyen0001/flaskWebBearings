import base64


def file_to_base64(file_content):
    picture_str = base64.b64encode(file_content).decode()
    return picture_str
