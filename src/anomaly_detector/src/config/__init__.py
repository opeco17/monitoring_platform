import argparse
import sys


if 'unittest' in sys.argv[0]:
    is_local = True if '--local' in sys.argv[-1] else False
else:
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true')
    args = parser.parse_args()
    is_local = args.local

if is_local:
    from config.local import Config
else:
    from config.prod import Config