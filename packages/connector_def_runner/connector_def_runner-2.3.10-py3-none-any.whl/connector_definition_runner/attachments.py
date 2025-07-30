import io
import re
import cgi
import urllib.parse
from email.message import Message


FILENAME_HEADER_KEY = 'Content-Disposition'
FILENAME_REGEX = """filename=['"]?([^"']*)['"]"""

def parse_content_disposition(header: str):
    # Create a Message instance to leverage its header parsing capabilities
    message = Message()
    message[FILENAME_HEADER_KEY] = header

    # Extract all parameters from the "Content-Disposition" header, including the disposition type
    params = message.get_params(header=FILENAME_HEADER_KEY)

    # Check if the first parameter is a valid disposition type (either "attachment" or "inline")
    if params is not None and len(params) > 0 and len(params[0]) > 0 and (params[0][0] == 'attachment' or params[0][0] == 'inline'):
        # Set the disposition to the first parameter's name (either "attachment" or "inline")
        disposition = params[0][0]
        # Exclude the first item (disposition type) from the parameters list
        params = params[1:]
    else:
        # If no disposition type is present, default to "attachment"
        disposition = 'attachment'

    # Convert the remaining parameters into a dictionary and return the disposition and parameters
    return disposition, dict(params)

def get_filename(response):
    """ 
    Gets filename from Content-Disposition Header.
    """
    cd_string = response.headers[FILENAME_HEADER_KEY]
    
    # Check if disposition is present
    if cd_string and cd_string.strip().split(';', 1)[0] not in ('attachment', 'inline'):
        _, params = parse_content_disposition(cd_string)
    else:
        _, params = cgi.parse_header(cd_string)

    if 'filename' in params:
        fname = params['filename']
    elif 'filename*' in params:
        fname = params['filename*']
    else:
        fname = "unknown"
    if "utf-8''" in fname.lower():
        fname = re.sub("utf-8''", '', fname, flags=re.IGNORECASE)
        fname = urllib.parse.unquote(fname)
    # clean space and double quotes
    return fname.strip().strip('"')


def get_file_object(response):
    return {
        'filename': get_filename(response),
        'file_data': io.BytesIO(response.content)
    }


def parse_attachment_output(response, manifest):
    if 'file' not in manifest['output'].get('properties', {}):
        return

    if manifest['output']['properties']['file']['type'] == 'array':
        return [get_file_object(response)]
    else:
        return get_file_object(response)
