from common import config, data_handler
from helper import raw_data_helper
from policy import base_point, break_point, pre_enter_point, key_point, enter_point, bonus_point
import csv


def go():
    tx5_dir = raw_data_helper.list_raw_dir(config.TX5_DIR)
    raw_data_helper.csv_write_header('max_min_total', get_out_key())

    for key in sorted(tx5_dir.keys()):
        for p in range(len(tx5_dir[key])):
            trace(tx5_dir[key][p])


def trace(tx5_file):
    # print(tx5_file)
    tx5_data = raw_data_helper.get_data(tx5_file)

    # print (tx5_data)
    max_min_point = get_max_min_point(tx5_data)
    diff = max_min_point['max'] - max_min_point['min']

    # print(tx1_data[0])
    out = {'date': tx5_data[0][data_handler.DATA_DATE],
           'max': max_min_point['max'],
           'max_time': max_min_point['max_time'],
           'min': max_min_point['min'],
           'min_time': max_min_point['min_time'],
           'diff': diff}

    # raw_data_helper.csv_write_row('max_min_' + month, get_out_key(), out)
    raw_data_helper.csv_write_row('max_min_total', get_out_key(), out)


def get_max_min_point(data):
    max_value = 0
    max_time = ''
    min_value = 1000000
    min_time = ''
    for i in range(len(data)):
        min_v = int(data[i][raw_data_helper.DATA_MIN_VALUE])
        max_v = int(data[i][raw_data_helper.DATA_MAX_VALUE])
        time = data[i][raw_data_helper.DATA_TIME]

        if max_v > max_value:
            max_value = max_v
            max_time = time

        if min_v < min_value:
            min_value = min_v
            min_time = time

    return {'max': max_value, 'max_time': max_time, 'min': min_value, 'min_time': min_time}


def get_out_key():
    return ['date', 'max', 'max_time', 'min', 'min_time', 'diff']
