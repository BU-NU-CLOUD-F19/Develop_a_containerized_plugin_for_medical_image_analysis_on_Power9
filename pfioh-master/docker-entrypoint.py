#!/usr/bin/env python3

# Single entry point / dispatcher for simplified running of
#
## pman
## pfioh
## purl
#

import  argparse
import  os

str_desc = """

 NAME

    docker-entrypoint.py

 SYNOPSIS

    docker-entrypoint.py    [optional cmd args for pfioh]


 DESCRIPTION

    'docker-entrypoint.py' is the main entry point for running the pfioh container.

"""

def pfioh_do(args, unknown):

    str_otherArgs   = ' '.join(unknown)

    str_CMD = "/usr/local/bin/pfioh --forever %s" % (str_otherArgs)
    return str_CMD

parser  = argparse.ArgumentParser(description = str_desc)

parser.add_argument(
    '--msg',
    action  = 'store',
    dest    = 'msg',
    default = '',
    help    = 'JSON msg payload'
)

args, unknown   = parser.parse_known_args()

if __name__ == '__main__':
    try:
        fname   = 'pfioh_do(args, unknown)'
        str_cmd = eval(fname)
        # print(str_cmd)
        os.system(str_cmd)
    except:
        print("Misunderstood container app... exiting.")
