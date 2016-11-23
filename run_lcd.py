#!/usr/bin/env python
import time
import sys
import os
import stat
import logging
import urllib2

import LCD1602 as LCD

from optparse import OptionParser

NOAA_URL='http://tgftp.nws.noaa.gov/data/observations/metar/stations/'


def setup():
    LCD.init(0x27, 1) # init(slave address, background light)
    LCD.write(1, 0, 'Beginning the') # write(x, y, data)
    LCD.write(1, 1, 'METAR Loop!')
    time.sleep(2)


def fetch_metar(options, station):
    """ Fetches METAR data from NOAA based on the supplied station ID.
        We don't retry, it will try the fetch again when options.cache expires
    """

    url = NOAA_URL + station + '.TXT'
    if options.debug:
        logging.debug("Fetching " + url)
    try:
        response = urllib2.urlopen(url)
    except urllib2.URLError, err:
        logging.error(err.reason)
        return None

    data = response.read()
    if options.debug:
        logging.debug("URL data fetched: " + data)
    try:
        parsed = data.splitlines()[1:2][0] # date is first, data is second line
    except KeyError:
        parsed = None

    return parsed


def metars(options):
    """ prints data in a scrolling fashion to the LCD, which holds 16 chars
        across, by printing chars 1-16 on the top, 17-32 on the bottom,
        then shifting left one until done.
    """
    path = options.station + '.TXT'
    data = None
    cache_exists = False
    cache_expired = False
    using_stale = False

    try:
        os.stat(path)
        cache_exists = True
    except OSError:
        pass

    # check file age, update if necessary:
    if cache_exists and (time.time() - os.stat(path)[stat.ST_MTIME]) > options.cache:
        cache_expired = True
        data = fetch_metar(options, options.station)
    elif not cache_exists:
        data = fetch_metar(options, options.station)

    # data can be None if url fetching failed... OK to use old cache in this case
    if not data and cache_exists:
        with open(path, 'r') as fh:
            data = fh.readline()
        using_stale = True

    # finally, we have no cache, and the URL fetch probably failed:
    elif not data:
        if options.debug:
            logging.debug("no data, and the URL fetch failed, sleeping for 60 seconds")
        time.sleep(60)
        return False

    # we have data, write to cache if it's expired, or didn't exist (skip if we're
    # intentionally using stale data, to avoid freshening it with a write):
    if not using_stale and (not cache_exists or cache_expired):
        with open(path, 'w') as fh:
            fh.write(data)

    while True:
        if options.single_line:
            top = "METAR " + options.station + " @ " + data.split()[1]
            LCD.write(0, 0, top[:16])
        else:
            top = data
        bottom = data
        for i in range(0, len(data)):
            if not options.single_line:
                LCD.write(0, 0, top[:16])
            LCD.write(0, 1, bottom[16:32])
            top = top[1:]
            bottom = bottom[1:]
            time.sleep(0.8)
            LCD.clear()


def destroy():
    LCD.clear()
    pass    


if __name__ == "__main__":
    parser = OptionParser(usage=__doc__)
    parser.add_option("-d", "--debug", help="Print debug messages.", action="store_true",
                      dest="debug")
    parser.add_option("-s", "--station", default="KCXP", help="METAR Station ID")
    parser.add_option("-c", "--cache", default=600,
                      help="Amount of time (in seconds) to use cached data from NOAA. They"
                           " update every 5 mins.")
    parser.add_option("--single-line", action='store_true',
                      help="Display scrolling METAR data on 2nd line, and station info"
                           "on first")
    (options, args) = parser.parse_args()

    if options.debug:
        log_level = logging.DEBUG
        logging.basicConfig(stream=sys.stdout, level=log_level)
    else:
        log_level = None
        logging.basicConfig(stream=sys.stdout, level=log_level)
        logging.basicConfig(stream=sys.stderr, level=(logging.ERROR, logging.CRITICAL))


    try:
        #example_loop()
        while True:
            setup()
            metars(options)
    except KeyboardInterrupt:
        destroy()
