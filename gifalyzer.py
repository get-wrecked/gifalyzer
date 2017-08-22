#!./venv/bin/python

import argparse
import os
import pprint

from PIL import Image


def main():
    args = get_args()
    report = analyze_gif(args.gif)
    print_report(report)


def print_report(report):
    longest_report_key = max(len(key) for key in report)
    for key, value in sorted(report.items()):
        print('%s: %s' % (key.ljust(longest_report_key), value))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('gif', help='Path to a gif to analyze')
    return parser.parse_args()


def analyze_gif(filepath):
    filesize = os.stat(filepath).st_size
    image = Image.open(filepath)
    pre_frames_loop = image.info.get('loop')
    initial_report = {
        'dimensions': image.size,
        'filesize': filesize,
        'humanized_filesize': humanize_size(filesize),
        'gif_version': image.info['version'],
        'frame_delay_ms': image.info['duration'],
    }

    if image.info['duration']:
        initial_report['frame_frequency'] = 1000/image.info['duration']

    frame_count = seek_to_last_frame(image)

    post_frames_loop = image.info.get('loop')

    if pre_frames_loop is not None:
        initial_report['loop'] = pre_frames_loop
    elif post_frames_loop is not None:
            initial_report['loop'] = '%d (extension block after frames)' % post_frames_loop
    else:
        initial_report['loop'] = 'No'

    total_duration_ms = initial_report['frame_delay_ms'] * frame_count + image.info['duration']
    initial_report['total_duration_ms'] = total_duration_ms

    initial_report['last_frame_delay_ms'] = image.info['duration']
    initial_report['frame_count'] = frame_count

    return initial_report


def seek_to_last_frame(image):
    frame_count = 1
    try:
        while True:
            image.seek(image.tell() + 1)
            frame_count += 1
    except EOFError:
        pass

    return frame_count


def humanize_size(size):
    suffixes = ['']
    suffixes.extend(list('kMGTP'))
    suffix_index = 0
    size = float(size)
    while size > 1200:
        size /= 1024
        suffix_index += 1
    return '%.1f%sB' % (size, suffixes[suffix_index])


if __name__ == '__main__':
    main()
