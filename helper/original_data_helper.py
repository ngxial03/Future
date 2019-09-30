from os import listdir
from common import config
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


def csv_write_header(dir, f_name, header):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    # print(config.OUT + '/' + f_name + '.csv')
    with open(dir + '/' + f_name + '.txt', 'a', newline='') as f:
        w = csv.DictWriter(f, header)
        w.writeheader()


def csv_write_row(dir, f_name, header, out):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    with open(dir + '/' + f_name + '.txt', 'a', newline='') as f:
        w = csv.DictWriter(f, header)
        w.writerow(out)
