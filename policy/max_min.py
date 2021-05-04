import datetime

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

    trace_max_min_times()


def trace(tx5_file):
    # print(tx5_file)
    tx5_data = raw_data_helper.get_data(tx5_file)

    # print (tx5_data)
    # max_min_point = get_max_min_point(tx5_data)
    max_min_point = get_max_min_point_after_index(tx5_data, 0)
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


def trace_max_min_times():
    raw_data_helper.csv_write_header('max_min_times', get_times_out_key())

    max_min_total = raw_data_helper.get_data('out/max_min_total.csv')
    # print(max_min_total)

    for i in range(61):
        # init_t = datetime.time(8, 45, 0)
        init_t = datetime.datetime.strptime('08:45:00', '%H:%M:%S')

        t = init_t + datetime.timedelta(hours=0, minutes=5 * i, seconds=0)
        t_str = t.strftime('%H:%M:%S')
        # print(t_str)

        max_min_times = get_max_min_times(max_min_total, t_str)
        # print(max_min_times)
        raw_data_helper.csv_write_row('max_min_times', get_times_out_key(), max_min_times)


def get_max_min_point_after_index(data, index):
    max_value = 0
    max_time = ''
    min_value = 1000000
    min_time = ''
    for i in range(len(data)):
        if i < index:
            continue

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


def get_max_min_times(data, time):
    max_times = 0
    min_times = 0

    for i in range(len(data)):
        max_v = int(data[i][1])
        max_time = data[i][2]
        min_v = int(data[i][3])
        min_time = data[i][4]

        if max_time == time:
            max_times = max_times + 1

        if min_time == time:
            min_times = min_times + 1

        # print(max_time)
        max_ss = max_time.split(':')
        min_ss = min_time.split(':')

        if (int(max_ss[0]) < 8) or (int(max_ss[0]) > 13):
            print(data[i][0])

        if (int(max_ss[2]) != 0) or (int(min_ss[2]) != 0):
            print(data[i][0])

        if (int(max_ss[1]) % 5 != 0) or (int(min_ss[1]) % 5 != 0):
            print(max_ss)
            print(min_ss)
            print(data[i][0])
            print('----')

    s = max_times + min_times

    return {'time': time, 'max_times': max_times, 'min_times': min_times, 'sum': s}


def get_times_out_key():
    return ['time', 'max_times', 'min_times', 'sum']
