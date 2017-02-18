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
    rootdir_pattern = re.compile('^.*?/devices')
    internal_devices = []

    def device_state(name):
        """
        Follow pmount policy to determine whether a device is removable or internal.
        """
        with open('/sys/block/%s/device/block/%s/removable' % (name, name)) as f:
            if f.read(1) == '1':
                return

        path = rootdir_pattern.sub('', os.readlink('/sys/block/%s' % name))
        hotplug_buses = ("usb", "ieee1394", "mmc", "pcmcia", "firewire")
        for bus in hotplug_buses:
            if os.path.exists('/sys/bus/%s' % bus):
                for device_bus in os.listdir('/sys/bus/%s/devices' % bus):
                    device_link = rootdir_pattern.sub('', os.readlink(
                        '/sys/bus/%s/devices/%s' % (bus, device_bus)))
                    if re.search(device_link, path):
                        return

        internal_devices.append(name)

    for path in glob('/sys/block/*/device'):
        name = re.sub('.*/(.*?)/device', '\g<1>', path)
        device_state(name)
    print(' '.join(internal_devices))
    return internal_devices


def hddinfo(hddev):
    if os.geteuid() > 0:
        print("ERROR: Must be root to use")

    with open(hddev, "rb") as fd:
        # tediously derived from the monster struct defined in <hdreg.h>
        # see comment at end of file to verify
        hd_driveid_format_str = "@ 10H 20s 3H 8s 40s 2B H 2B H 4B 6H 2B I 36H I Q 152H"
        # Also from <hdreg.h>
        HDIO_GET_IDENTITY = 0x030d
        # How big a buffer do we need?
        sizeof_hd_driveid = struct.calcsize(hd_driveid_format_str)

        # ensure our format string is the correct size
        # 512 is extracted using sizeof(struct hd_id) in the c code
        assert sizeof_hd_driveid == 512

        # Call native function
        buf = fcntl.ioctl(fd, HDIO_GET_IDENTITY, " " * sizeof_hd_driveid)
        fields = struct.unpack(hd_driveid_format_str, buf)
        serial_no = fields[10].strip()
        model = fields[15].strip()
        print("Hard Disk Model: %s" % model)
        print("  Serial Number: %s" % serial_no)

while True:
    check_for_update()
    restart_if_modified()
    get_disk()
    # hddinfo('/dev/sda')
    time.sleep(1)

    print datetime.now()
