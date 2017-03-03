# coding: utf-8
from subprocess import check_output
import os
import json
import itertools


def get_hdd_info():
    """
    Run "inxi -Dxx" command get HDD info and put to a variable

    :return: Path of the text file
    :rtype: str
    """
    inxi_output = None
    # Command get Serial Number
    arg1 = ['inxi', '-Dxx']
    try:
        inxi_output = check_output(arg1)
    except Exception as ex:
        print "{}".format(ex)

    # return path files
    return inxi_output


def parse_file():
    """
    Parse a variable get HDD info, convert to JSON

    :return: HDD info in Json type
    :rtype: json
    """
    data = {}
    inxi_output = get_hdd_info()

    try:
        # Read HDD information
        for line in inxi_output.split('\n'):
            if line == "":
                break
            elif line.startswith("Drives"):
                data[line.strip().split(":")[1].strip()] = line.strip().split(":")[2].strip()
            else:
                data[line.strip().split()[2]] = dict(
                    itertools.izip_longest(*[iter(line.strip().split()[1:])] * 2, fillvalue=""))

    except Exception as ex:
        print "{}".format(ex)
    return json.dumps(data)


if __name__ == '__main__':
    parse_file()
