# coding: utf-8
import os
import json
import itertools


def get_hdd_info():
    """
    Run "inxi -Dxx" command get HDD info and put to a text file

    :return: Path of the text file
    :rtype: str
    """
    inxi_output = None
    ls_output = None
    df_output = None

    # Command get informations of HDD
    arg1 = 'inxi -Dxx'
    arg2 = 'ls -lah /dev/vp9*[!^1]'
    arg3 = 'df -h |  grep /dev/'
    try:
        inxi_output = os.popen(arg1).readlines()
        ls_output = os.popen(arg2).readlines()
        df_output = os.popen(arg3).readlines()
    except Exception as ex:
        print "{}".format(ex)

    # return the variables
    return inxi_output, ls_output, df_output


def parse_file():
    """
    Parse file text get HDD info, convert to JSON

    :return: HDD info in Json type
    :rtype: json
    """
    data_inxi = {}
    inxi_output, ls_output, df_output = get_hdd_info()

    try:
        # Read information from inxi command
        for item in inxi_output:
            if item.strip() == "":
                break
            elif item.strip().startswith("Drives"):
                continue
            else:
                item = item.replace(":", "")
                item = item.strip().split()
                data_inxi[item[-3]] = dict(itertools.izip_longest(*[iter(item[1:])] * 2, fillvalue=""))

        # Read information from ls command and combine with data_inxi
        for item in ls_output:
            if item.strip() == "":
                break
            item = item.strip().split()
            for serial in data_inxi:
                if item[-1] in data_inxi[serial]['id']:
                    data_inxi[serial]['name'] = item[-3].split('/')[-1]
                    break

        # Read information from df command and combine with data_inxi
        for item in df_output:
            if item.strip() == "":
                break
            item = item.strip().split()
            if item[-1] == '/':
                continue
            else:
                for serial in data_inxi:
                    if 'name' in data_inxi[serial].keys():
                        if item[-1].split('/')[-1] in data_inxi[serial]['name']:
                            data_inxi[serial]['mounted'] = item[-1]
                            data_inxi[serial]['size'] = item[1]
                            data_inxi[serial]['used'] = item[2]
                            data_inxi[serial]['avail'] = item[3]
                            data_inxi[serial]['use'] = item[4]
                            break
    except Exception as ex:
        print "{}".format(ex)
    print json.dumps(data_inxi)
    return json.dumps(data_inxi)


if __name__ == '__main__':
    parse_file()
