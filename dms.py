#!/usr/bin/python
import os
import sys
import time
from os.path import getmtime
from datetime import datetime

# Check modified time at startup
WATCHED_FILES = [__file__]
WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]


def check_for_update():
    pass


def restart_if_modified():
    # Check whether a watched file has modified.
    for f, mtime in WATCHED_FILES_MTIMES:
        if getmtime(f) != mtime:
            print('File modified, restarting')
            os.execv(__file__, sys.argv)

while True:
    check_for_update()
    restart_if_modified()
    time.sleep(1)
    print datetime.now()
