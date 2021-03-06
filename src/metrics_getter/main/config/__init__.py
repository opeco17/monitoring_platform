import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--local', action='store_true')
args = parser.parse_args()

if args.local:
    from config.local import Config
else:
    from config.prod import Conifg