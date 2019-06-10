import os
import json
import subprocess

from .util import humanize_size


def analyze_mp4(filepath):
    filesize = os.stat(filepath).st_size
    streams = json.loads(subprocess.check_output([
        'ffprobe',
        '-hide_banner',
        '-of', 'json',
        '-show_streams',
        '-select_streams', 'video',
        filepath,
        '-loglevel', 'warning',
    ]))['streams']
    if len(streams) != 1:
        raise ValueError('More than a single stream in file')

    stream = streams[0]
    report = {
        'dimensions': (stream['width'], stream['height']),
        'filesize': filesize,
        'humanized_filesize': humanize_size(filesize),
        'bitrate': humanize_bitrate(stream['bit_rate']),
        'profile': stream['profile'],
        'total_duration_ms': stream['duration'],
    }

    frames = json.loads(subprocess.check_output([
        'ffprobe',
        '-hide_banner',
        '-of', 'json',
        '-show_frames',
        filepath,
        '-loglevel', 'warning',
    ]))['frames']
    report['frame_count'] = len(frames)
    report['iframes'] = sum(frame['key_frame'] for frame in frames)
    last_frame = next(f for f in frames if f['coded_picture_number'] == len(frames) - 1)
    report['last_frame_delay_ms'] = float(last_frame['pkt_duration_time'])*1000
    report['reordered'] = frames != sorted(frames, key=lambda f: f['coded_picture_number'])

    return report


def humanize_bitrate(bitrate):
    suffixes = ['']
    suffixes.extend(list('kMGTP'))
    suffix_index = 0
    bitrate = float(bitrate)
    while bitrate > 1200:
        bitrate /= 1024
        suffix_index += 1
    return '%.1f%sbps' % (bitrate, suffixes[suffix_index])
