# coding: utf-8
from subprocess import call
import os
import json
import itertools


def get_hdd_info():
    """
    Run "inxi -Dxx" command get HDD info and put to a text file

    :return: Path of the text file
    :rtype: str
    """
    # Command get Serial Number
    arg1 = ["inxi -Dxx > inxi.txt"]
    try:
        call(arg1)
    except Exception as ex:
        print "{}".format(ex)

    # return path files
    inxi_path = os.path.dirname(os.path.realpath(__file__)) + "/inxi.txt"
    return inxi_path


def parse_file():
    """
    Parse file text get HDD info, convert to JSON

    :return: HDD info in Json type
    :rtype: json
    """
    data = {}
    inxi_hand = None
    inxi_path = get_hdd_info()
    try:
        # Read HDD information
        inxi_hand = open(inxi_path)
        for line in inxi_hand:
            if line.strip().startswith("Drives"):
                data[line.strip().split(":")[1].strip()] = line.strip().split(":")[2].strip()
            else:
                data[line.strip().split()[2]] = dict(itertools.izip_longest(*[iter(line.strip().split()[1:])] * 2, fillvalue=""))

    except IOError as io_error:
        inxi_hand.close()
        print "{}".format(io_error)
    return json.dumps(data)


if __name__ == '__main__':
    parse_file()
