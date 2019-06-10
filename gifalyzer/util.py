import os
import tempfile

import requests


def download_file(url):
    ext = os.path.splitext(url)[1]
    destination = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    response = requests.get(url, stream=True)
    chunk_size = 32*2**10
    with destination:
        for chunk in response.iter_content(chunk_size):
            destination.write(chunk)
    return destination.name


def humanize_size(size):
    suffixes = ['']
    suffixes.extend(list('kMGTP'))
    suffix_index = 0
    size = float(size)
    while size > 1200:
        size /= 1024
        suffix_index += 1
    return '%.1f%sB' % (size, suffixes[suffix_index])
