# -*- coding: utf-8 -*-
import argparse
import sys

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='filenames to check')
    args = parser.parse_args(argv)


    print(args.filenames)

    return_code = 0
    return return_code

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
