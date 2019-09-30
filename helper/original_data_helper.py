import sys
from os import listdir
import csv
import os

DATA_DATE = 0
DATA_PRODUCT = 1
DATA_TIME = 3
DATA_VALUE = 4
DATA_VOLUME = 5


def list_original_dir(d):
    out = []
    dirs = sorted([d + '/' + i for i in listdir(d)])
    for i in range(len(dirs)):
        if '.DS_Store' not in dirs[i]:
            out.append(dirs[i])
    return out


def get_data(f):
    data = open(f).readlines()
    data1 = [i.strip('\n').strip('\r').split(',') for i in data]
    return data1


def csv_write_header(month_dir, f_name, header):
    if not os.path.isdir(month_dir):
        os.mkdir(month_dir)
    kwargs = {}
    if sys.version_info[0] != 2:
        kwargs = {'newline': ''}
    with open(month_dir + '/' + f_name + '.txt', 'a', **kwargs) as f:
        w = csv.DictWriter(f, header)
        w.writeheader()


def csv_write_row(month_dir, f_name, header, out):
    if not os.path.isdir(month_dir):
        os.mkdir(month_dir)
    kwargs = {}
    if sys.version_info[0] != 2:
        kwargs = {'newline': ''}
    with open(month_dir + '/' + f_name + '.txt', 'a', **kwargs) as f:
        w = csv.DictWriter(f, header)
        w.writerow(out)
