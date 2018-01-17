import argparse
import os

from .gif import analyze_gif
from .png import analyze_png
from .util import download_file
from ._version import __version__


def main():
    args = get_args()
    is_tempfile = False
    if args.gif.startswith('http'):
        temp_path = download_file(args.gif)
        args.gif = temp_path
        is_tempfile = True
    try:
        if args.png:
            report = analyze_png(args.gif)
        else:
            report = analyze_gif(args.gif)
    finally:
        if is_tempfile:
            os.remove(args.gif)
    print_report(report)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('gif', help='Path or URL to a gif to analyze')
    parser.add_argument('-v', '--version', action='version',
        version='v%s' % __version__)
    parser.add_argument('--png', action='store_true', default=False)
    return parser.parse_args()


def print_report(report):
    longest_report_key = max(len(key) for key in report)
    for key, value in sorted(report.items()):
        print('%s: %s' % (key.ljust(longest_report_key), value))


if __name__ == '__main__':
    main()
