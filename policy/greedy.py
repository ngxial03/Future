from common import config, data_handler
from helper import raw_data_helper
import csv

# minutes
BASE_RANGE = 15  # 09:00:00
PRE_BREAK_INDEX = 10  # 08:55:00
BREAK_RANGE = 75  # 10:00:00
TERMINAL_TIME = 165  # 11:30:00

# points
PRE_BREAK_AMPLITUDE = 5
PRE_ENTER_AMPLITUDE = 0
PRE_BONUS_AMPLITUDE = 26
WIN_AMPLITUDE = 26
LOSE_AMPLITUDE = 26

# const
RETURN_SCALE = 3

# global
total_bonus = 0


def go():
    # writeTitle()

    tx1_dir = raw_data_helper.list_raw_dir(config.TX1_DIR)
    tx5_dir = raw_data_helper.list_raw_dir(config.TX5_DIR)
    # print(tx5_dir)

    raw_data_helper.csv_write_header('greedy_total', get_out_key())

    for key in tx1_dir:
        # print (key)
        # print (tx1_helper.get_tx1_data(tx1_dir[key][0]))
        raw_data_helper.csv_write_header('greedy_' + key, get_out_key())
        for p in range(len(tx1_dir[key])):
            trace(key, tx1_dir[key][p], tx5_dir[key][p])
            # break
        # break
    global total_bonus
    print(total_bonus)


def trace(month, tx1_file, tx5_file):
    # print(tx1_file)
    print(tx5_file)

    # dailyData = function2.getDailyData(config.TX_DAILY_DIR)
    tx1_data = raw_data_helper.get_data(tx1_file)
    tx5_data = raw_data_helper.get_data(tx5_file)

    base_point = get_base_point(tx5_data, BASE_RANGE // 5, PRE_BREAK_INDEX // 5, PRE_BREAK_AMPLITUDE)
    # print(base_point)

    break_point = get_break_point(tx5_data, PRE_BREAK_INDEX // 5, base_point)
    # print(break_point)

    pre_enter_point = get_pre_enter_point(tx1_data, PRE_BREAK_INDEX, base_point, PRE_ENTER_AMPLITUDE)

    out = {'date': tx1_data[0][data_handler.DATA_DATE],
           'base_max': base_point['max'],
           'base_min': base_point['min'],
           'break_max': break_point['max'],
           'break_min': break_point['min'],
           'break_last': break_point['last'],
           'direction': 'up' if break_point['direction'] == 0 else ('down' if break_point['direction'] == 1 else ''),
           'break_time': break_point['time'],
           'pre_enter_time': pre_enter_point['time'],
           'pre_enter_direction': 'up' if pre_enter_point['direction'] == 0 else ('down' if pre_enter_point['direction'] == 1 else ''),
           'pre_enter_point': pre_enter_point['point']}

    # print('\n')

    raw_data_helper.csv_write_row('greedy_' + month, get_out_key(), out)
    raw_data_helper.csv_write_row('greedy_total', get_out_key(), out)


def get_base_point(data, base_range, pre_break_index, per_break_amplitude):
    max_value = 0
    min_value = 1000000
    pre_break = False

    for i in range(base_range):
        # print(data[i])
        min_v = int(data[i][raw_data_helper.DATA_MIN_VALUE])
        max_v = int(data[i][raw_data_helper.DATA_MAX_VALUE])
        last_v = int(data[i][raw_data_helper.DATA_LAST_VALUE])

        if (max_v > max_value) & (i >= pre_break_index) & ((last_v - max_value) >= per_break_amplitude):
            pre_break = True
            break

        if (min_v < min_value) & (i >= pre_break_index) & ((min_value - last_v) >= per_break_amplitude):
            pre_break = True
            break

        if max_v > max_value:
            max_value = max_v

        if min_v < min_value:
            min_value = min_v

    index = 15 if pre_break else 10
    return {'max': max_value, 'min': min_value, 'pre_break': pre_break, 'diff': max_value - min_value, 'index': index}


def get_break_point(data, pre_break_index, base_point):
    break_index = -1
    direction = -1
    for i in range(pre_break_index, len(data)):
        last_value = int(data[i][raw_data_helper.DATA_LAST_VALUE])
        if last_value > int(base_point['max']):
            break_index = i
            direction = 0
            break
        if last_value < int(base_point['min']):
            break_index = i
            direction = 1
            break
    # break_index = get_break_index(data, pre_break_index, base_point)
    max_value = '' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_MAX_VALUE])
    min_value = '' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_MIN_VALUE])
    last_value = '' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_LAST_VALUE])
    time = '' if break_index == -1 else data[break_index][raw_data_helper.DATA_TIME]
    index = -1 if break_index == -1 else (break_index + 1) * 5
    diff = '' if break_index == -1 else max_value - min_value
    pre_enter = False
    pre_enter_point = 0

    # print(break_index)
    return {'max': max_value, 'min': min_value, 'last': last_value, 'time': time, 'diff': diff, 'index': index,
            'direction': direction}


def get_pre_enter_point(data, pre_break_index, base_point, pre_enter_amplitude):
    pre_enter_index = -1
    pre_enter_point = 0
    direction = -1
    for i in range(pre_break_index, len(data)):
        max_value = int(data[i][raw_data_helper.DATA_MAX_VALUE])
        min_value = int(data[i][raw_data_helper.DATA_MIN_VALUE])
        last_value = int(data[i][raw_data_helper.DATA_LAST_VALUE])
        if max_value >= int(base_point['max']) + pre_enter_amplitude:
            pre_enter_index = i
            pre_enter_point = int(base_point['max']) + pre_enter_amplitude
            direction = 0
            break
        if min_value <= int(base_point['min']) - pre_enter_amplitude:
            pre_enter_index = i
            pre_enter_point = int(base_point['min']) - pre_enter_amplitude
            direction = 1
            break

    time = '' if pre_enter_index == -1 else data[pre_enter_index][raw_data_helper.DATA_TIME]
    return {'time': time, 'index': pre_enter_index + 1, 'direction': direction, 'point': pre_enter_point}


def get_out_key():
    return ['date', 'base_max', 'base_min', 'break_max', 'break_min', 'break_last', 'direction', 'break_time',
            'pre_enter_time', 'pre_enter_direction', 'pre_enter_point']
