#!/usr/bin/python
import fcntl
import os
import struct
import sys
import time
import psutil
import json
import re
from glob import glob
from datetime import datetime
from os.path import getmtime

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


def get_disk():
    root_dir_pattern = re.compile('^.*?/devices')
    internal_devices = []

    def device_state(dev_name):
        with open('/sys/block/%s/device/block/%s/removable' % (name, name)) as f:
            if f.read(1) == '1':
                return
        dev_path = root_dir_pattern.sub('', os.readlink('/sys/block/%s' % name))
        hot_plug_buses = ("usb", "ieee1394", "mmc", "pcmcia", "firewire")
        for bus in hot_plug_buses:
            if os.path.exists('/sys/bus/%s' % bus):
                for device_bus in os.listdir('/sys/bus/%s/devices' % bus):
                    device_link = root_dir_pattern.sub('', os.readlink(
                        '/sys/bus/%s/devices/%s' % (bus, device_bus)))
                    if re.search(device_link, dev_path):
                        return

        internal_devices.append(dev_name)

    for path in glob('/sys/block/*/device'):
        name = re.sub('.*/(.*?)/device', '\g<1>', path)
        device_state(name)
    print(' '.join(internal_devices))
    return internal_devices


def hddinfo(hddev):
    pass

while True:
    check_for_update()
    restart_if_modified()
    get_disk()
    # hddinfo('/dev/sda')
    time.sleep(1)

    print datetime.now()
