import datetime

from common import config, data_handler
from helper import raw_data_helper
from policy import base_point, break_point, pre_enter_point, key_point, enter_point, bonus_point
import csv


def go():
    tx5_dir = raw_data_helper.list_raw_dir(config.TX5_DIR)
    raw_data_helper.csv_write_header('mm_max_min_detail', get_out_key())

    for key in sorted(tx5_dir.keys()):
        for p in range(len(tx5_dir[key])):
            trace(tx5_dir[key][p])


def trace(tx5_file):
    # print(tx5_file)
    tx5_data = raw_data_helper.get_data(tx5_file)

    # print (tx5_data)
    # max_min_point = get_max_min_point(tx5_data)
    max_min_point = get_max_min_point(tx5_data)
    diff = max_min_point['max'] - max_min_point['min']
    max_judge = judge_max(max_min_point)
    min_judge = judge_min(max_min_point)

    # print(tx1_data[0])
    out = {'date': tx5_data[0][data_handler.DATA_DATE],
           'max': max_min_point['max'],
           'max_time': max_min_point['max_time'],
           'max_open': max_min_point['max_open'],
           'max_close': max_min_point['max_close'],
           'max_min': max_min_point['max_min'],
           'max_judge': max_judge,
           'min': max_min_point['min'],
           'min_time': max_min_point['min_time'],
           'min_open': max_min_point['min_open'],
           'min_close': max_min_point['min_close'],
           'min_max': max_min_point['min_max'],
           'min_judge': min_judge
           }

    # raw_data_helper.csv_write_row('max_min_' + month, get_out_key(), out)
    raw_data_helper.csv_write_row('mm_max_min_detail', get_out_key(), out)


def get_max_min_point(data):
    max_value = 0
    max_time = ''
    max_open = 0
    max_close = 0
    max_min_value = 0

    min_value = 1000000
    min_time = ''
    min_open = 0
    min_close = 0
    min_max_value = 0

    for i in range(len(data)):
        min_v = int(data[i][raw_data_helper.DATA_MIN_VALUE])
        max_v = int(data[i][raw_data_helper.DATA_MAX_VALUE])
        open_v = int(data[i][raw_data_helper.DATA_OPEN_VALUE])
        close_v = int(data[i][raw_data_helper.DATA_LAST_VALUE])
        time = data[i][raw_data_helper.DATA_TIME]

        if max_v > max_value:
            max_value = max_v
            max_time = time
            max_open = open_v
            max_close = close_v
            max_min = min_v

        if min_v < min_value:
            min_value = min_v
            min_time = time
            min_open = open_v
            min_close = close_v
            min_max = max_v

    return {'max': max_value, 'max_time': max_time, 'max_open': max_open, 'max_close': max_close, 'max_min': max_min,
            'min': min_value, 'min_time': min_time, 'min_open': min_open, 'min_close': min_close, 'min_max': min_max}


def get_out_key():
    return ['date', 'max', 'max_time', 'max_open', 'max_close', 'max_min', 'max_judge', 'min', 'min_time', 'min_open',
            'min_close', 'min_max', 'min_judge']


def judge_max(max_min_point):
    max_v = int(max_min_point['max'])
    min_v = int(max_min_point['max_min'])
    open_v = int(max_min_point['max_open'])
    close_v = int(max_min_point['max_close'])
    down_power = 0
    up_power = 0
    if close_v < open_v:
        down_power = max_v - close_v
        up_power = close_v - min_v
    else:
        down_power = max_v - close_v
        up_power = close_v - min_v

    ratio = 0
    if up_power == 0:
        ratio = 99999999
    else:
        ratio = float(down_power) / up_power
    return ratio


def judge_min(max_min_point):
    max_v = int(max_min_point['min_max'])
    min_v = int(max_min_point['min'])
    open_v = int(max_min_point['min_open'])
    close_v = int(max_min_point['min_close'])
    down_power = 0
    up_power = 0
    if close_v < open_v:
        down_power = max_v - close_v
        up_power = close_v - min_v
    else:
        down_power = max_v - close_v
        up_power = close_v - min_v

    ratio = 0
    if down_power == 0:
        ratio = 99999999
    else:
        ratio = float(up_power) / down_power
    return ratio
