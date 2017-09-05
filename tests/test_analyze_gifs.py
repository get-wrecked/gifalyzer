import os

import pytest

from gifalyzer import analyze_gif


def test_analyze_gifs_normal():
    report = analyze_gif(get_sample('200x202-26-130-130-0.gif'))
    assert report['dimensions'] == (200, 202)
    assert report['frame_count'] == 26
    assert report['frame_delay_ms'] == 130
    assert report['last_frame_delay_ms'] == 130
    assert report['loop'] == 0


def get_sample(sample_name):
    sample_dir = os.path.join(os.path.dirname(__file__), 'samples')
    return os.path.join(sample_dir, sample_name)
