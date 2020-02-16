import sys
from datetime import datetime
from os import listdir

from matplotlib.dates import date2num

from common import config
import csv

DATA_DATE = 0
DATA_TIME = 1
DATA_OPEN_VALUE = 2
DATA_MAX_VALUE = 3
DATA_MIN_VALUE = 4
DATA_LAST_VALUE = 5
DATA_VOLUME = 6


def list_raw_dir(d):
    month_dir_list = list_dir(d)
    dicts = {}
    for i in range(len(month_dir_list)):
        dicts[month_dir_list[i][9:15]] = list_dir(month_dir_list[i])
    return dicts


def list_dir(d):
    out = []
    dirs = sorted([d + '/' + i for i in listdir(d)])
    for i in range(len(dirs)):
        if '.DS_Store' not in dirs[i]:
            out.append(dirs[i])
    return out


def get_data(f):
    data = open(f).readlines()
    data[0:1] = ()
    data1 = [i.strip('\n').strip('\r').split(',') for i in data]
    return data1


def transfer(d):
    dic = {"time": [], "High": [], "Low": [], "Open": [], "Close": []}
    for i in range(0, len(d)):
        t_value = d[i][DATA_TIME]
        # float_t = float(t_value.replace(":", ""))
        open_value = int(d[i][DATA_OPEN_VALUE])
        last_value = int(d[i][DATA_LAST_VALUE])
        max_value = int(d[i][DATA_MAX_VALUE])
        min_value = int(d[i][DATA_MIN_VALUE])
        dic["time"].append(t_value)
        dic["High"].append(max_value)
        dic["Low"].append(min_value)
        dic["Open"].append(open_value)
        dic["Close"].append(last_value)
    return dic


def csv_write_header(f_name, header):
    # print(config.OUT + '/' + f_name + '.csv')
    kwargs = {}
    if sys.version_info[0] != 2:
        kwargs = {'newline': ''}
    with open(config.OUT + '/' + f_name + '.csv', 'a', **kwargs) as f:
        w = csv.DictWriter(f, header)
        w.writeheader()


def csv_write_row(f_name, header, out):
    kwargs = {}
    if sys.version_info[0] != 2:
        kwargs = {'newline': ''}
    with open(config.OUT + '/' + f_name + '.csv', 'a', **kwargs) as f:
        w = csv.DictWriter(f, header)
        w.writerow(out)
