import tempfile

import requests


def download_file(url):
    destination = tempfile.NamedTemporaryFile(delete=False)
    response = requests.get(url, stream=True)
    chunk_size = 32*2**10
    with destination:
        for chunk in response.iter_content(chunk_size):
            destination.write(chunk)
    return destination.name
