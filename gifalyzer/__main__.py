import argparse
import os

from .gif import analyze_gif
from .util import download_file
from ._version import __version__


def main():
    args = get_args()
    is_tempfile = False
    if should_download(args.gif):
        temp_path = download_file(args.gif)
        args.gif = temp_path
        is_tempfile = True
    try:
        report = analyze_gif(args.gif, args.dump_palette)
    finally:
        if is_tempfile:
            os.remove(args.gif)
    print_report(report)


def should_download(gif_path):
    if os.path.exists(gif_path):
        return False

    return gif_path.startswith('https://') or gif_path.startswith('http://')


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('gif', help='Path or URL to a gif to analyze')
    parser.add_argument('-v', '--version', action='version',
        version='v%s' % __version__)
    parser.add_argument('-p', '--dump-palette', action='store_true',
        help='Whether to dump the palette to a png')
    return parser.parse_args()


def print_report(report):
    longest_report_key = max(len(key) for key in report)
    for key, value in sorted(report.items()):
        print('%s: %s' % (key.ljust(longest_report_key), value))


if __name__ == '__main__':
    main()
