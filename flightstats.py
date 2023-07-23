#!/usr/bin/env python3

import math
import sys
import subprocess
import igc
import argparse
import json

from constants import *
import landepunkt

parser = argparse.ArgumentParser(description="TODO")
parser.add_argument("-i", type=str, help="Gzipped IGC file to read", required=True)
args = parser.parse_args()

gunzip = subprocess.Popen(("gunzip",), stdin=open(args.i), stdout=subprocess.PIPE)
track = igc.parse(gunzip.stdout)

p = landepunkt.landepunkt(track)
landepunktabstand = landepunkt.landepunktabstand(p)


json.dump(
    {
        "landepunkt": p,
        "landepunktabstand": landepunktabstand,
    },
    sys.stdout,
    indent=True,
)
