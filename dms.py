#!/usr/bin/python
import os
import sys
import time
import psutil
import json
import re
from urllib2 import urlopen
from glob import glob
from datetime import datetime
from os.path import getmtime

version = 1
update_url = "http://vnexpress.net"
# Check modified time at startup
WATCHED_FILES = [__file__]
WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]


def download(url):
    file_name = url.split('/')[-1]
    u = urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8) * (len(status) + 1)
        print status,

    f.close()

def check_for_update():
    download(update_url)



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
    # print(' '.join(internal_devices))
    return internal_devices


def hddinfo(hddev):
    print os.stat(hddev).st_size
    # pass

while True:
    check_for_update()
    restart_if_modified()
    print get_disk()
    hddinfo('/dev/sda')
    time.sleep(1)
    print datetime.now()
