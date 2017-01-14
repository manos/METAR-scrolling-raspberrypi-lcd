#!/usr/bin/env python
from optparse import OptionParser
from run_lcd import fetch_metar


if __name__ == "__main__":
    parser = OptionParser(usage=__doc__)
    parser.add_option("-d", "--debug", help="Print debug messages.", action="store_true")
    parser.add_option("-s", "--station", default="KCXP", help="METAR Station ID")
    (options, args) = parser.parse_args()

    print(fetch_metar(options, options.station))
