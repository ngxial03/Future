from common import config, data_handler
from helper import raw_data_helper
import csv

# minutes
BASE_RANGE = 15  # 09:00:00
PRE_BREAK_INDEX = 10  # 08:55:00
BREAK_RANGE = 75  # 10:00:00
TERMINAL_TIME = 165  # 11:30:00

# points
PRE_BREAK_AMPLITUDE = 0
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

    raw_data_helper.csv_write_header('happy_total', get_out_key())

    for key in tx1_dir:
        # print (key)
        # print (tx1_helper.get_tx1_data(tx1_dir[key][0]))
        raw_data_helper.csv_write_header('happy_' + key, get_out_key())
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

    break_point = get_break_point(tx5_data, PRE_BREAK_INDEX // 5, base_point, PRE_ENTER_AMPLITUDE)
    # print(break_point)

    key_point = get_key_point(break_point, RETURN_SCALE)
    # print(key_point)

    enter_point = get_enter_point(tx1_data, break_point, key_point, BREAK_RANGE)
    # print(enter_point)

    bonus_point = get_bonus_point(tx1_data, enter_point, key_point, TERMINAL_TIME, PRE_BONUS_AMPLITUDE, WIN_AMPLITUDE,
                                  LOSE_AMPLITUDE)
    # print(bonus_point)
    global total_bonus
    if bonus_point['bonus'] != '':
        total_bonus = total_bonus + int(bonus_point['bonus'])

    out = {'date': tx1_data[0][data_handler.DATA_DATE],
           'base_max': base_point['max'],
           'base_min': base_point['min'],
           'break_max': break_point['max'],
           'break_min': break_point['min'],
           'direction': 'up' if break_point['direction'] == 0 else ('down' if break_point['direction'] == 1 else ''),
           'break_time': break_point['time'],
           'pre_enter': '' if break_point['index'] == -1 else break_point['pre_enter'],
           'key_point': key_point,
           'enter_time': enter_point['time'],
           'bonus': bonus_point['bonus'],
           'bonus_time': bonus_point['time'],
           'max_bonus': bonus_point['max_bonus'],
           'max_bonus_time': bonus_point['max_bonus_time'],
           'max_lose': bonus_point['max_lose'],
           'max_lose_time': bonus_point['max_lose_time']}

    # print('\n')

    raw_data_helper.csv_write_row('happy_' + month, get_out_key(), out)
    raw_data_helper.csv_write_row('happy_total', get_out_key(), out)


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


def get_break_point(data, pre_break_index, base_point, pre_enter_amplitude):
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
    time = '' if break_index == -1 else data[break_index][raw_data_helper.DATA_TIME]
    index = -1 if break_index == -1 else (break_index + 1) * 5
    diff = '' if break_index == -1 else max_value - min_value
    pre_enter = False
    pre_enter_point = 0
    if break_index != -1:
        if (direction == 0) & (max_value - int(base_point['max']) >= pre_enter_amplitude):
            pre_enter_point = int(base_point['max']) + pre_enter_amplitude
            pre_enter = True

        if (direction == 1) & (int(base_point['min']) - min_value >= pre_enter_amplitude):
            pre_enter_point = int(base_point['min']) - pre_enter_amplitude
            pre_enter = True

    # print(break_index)
    return {'max': max_value, 'min': min_value, 'time': time, 'diff': diff, 'index': index,
            'direction': direction, 'pre_enter': pre_enter, 'pre_enter_point': pre_enter_point}


def get_key_point(break_point, return_scale):
    key_point = -1
    if break_point['index'] != -1:
        return_value = break_point['diff'] // return_scale
        key_point = (break_point['max'] - return_value) if break_point['direction'] == 0 else break_point[
                                                                                                  'min'] + return_value
    if break_point['pre_enter']:
        key_point = break_point['pre_enter_point']
    return '' if key_point == -1 else key_point


def get_enter_point(data, break_point, key_point, break_range):
    index = -1
    # print(break_point['index'])
    if (break_point['index'] != -1) & (break_point['index'] < break_range):
        r = break_point['index']
        if break_point['pre_enter']:
            r = r - 5

        for i in range(r, len(data)):
            if break_point['direction'] == 0:
                min_v = int(data[i][raw_data_helper.DATA_MIN_VALUE])
                if min_v <= key_point:
                    index = i
                    break
            if break_point['direction'] == 1:
                max_v = int(data[i][raw_data_helper.DATA_MAX_VALUE])
                if max_v >= key_point:
                    index = i
                    break

    max_value = '' if (break_point['index'] == -1) | (break_point['index'] >= break_range) else int(
        data[index][raw_data_helper.DATA_MAX_VALUE])
    min_value = '' if (break_point['index'] == -1) | (break_point['index'] >= break_range) else int(
        data[index][raw_data_helper.DATA_MIN_VALUE])
    time = '' if (break_point['index'] == -1) | (break_point['index'] >= break_range) else data[index][
        raw_data_helper.DATA_TIME]
    index = -1 if index == -1 else index + 1
    return {'max': max_value, 'min': min_value, 'time': time, 'index': index, 'direction': break_point['direction']}


def get_bonus_point(data, enter_point, key_point, terminal_time, pre_bonus_amplitude, win_amplitude, lose_amplitude):
    bonus = -100000
    bonus_time = ''
    max_bonus = -100000
    max_bonus_time = ''
    max_lose = -100000
    max_lose_time = ''

    if enter_point['index'] != -1:
        # print(enter_point['index'])
        for i in range(enter_point['index'] - 1, len(data)):
            time = data[i][raw_data_helper.DATA_TIME]
            max_value = int(data[i][raw_data_helper.DATA_MAX_VALUE])
            min_value = int(data[i][raw_data_helper.DATA_MIN_VALUE])
            last_value = int(data[i][raw_data_helper.DATA_LAST_VALUE])
            win = 0
            lose = 0

            if enter_point['direction'] == 0:
                lose = key_point - min_value
                win = max_value - key_point

            if enter_point['direction'] == 1:
                lose = max_value - key_point
                win = key_point - min_value

            if win > max_bonus:
                max_bonus = win
                max_bonus_time = time

            if lose > max_lose:
                max_lose = lose
                max_lose_time = time

            if (lose > 0) & (max_bonus >= pre_bonus_amplitude):
                bonus = 1
                bonus_time = time
                break

            if (win >= win_amplitude) & (bonus == -100000):
                bonus = win_amplitude
                bonus_time = time
                break

            if (lose >= lose_amplitude) & (bonus == -100000):
                bonus = -1 * lose_amplitude
                bonus_time = time
                break

            if i >= terminal_time - 1:
                if bonus == -100000:
                    bonus_time = time
                    if enter_point['direction'] == 0:
                        bonus = last_value - key_point
                    if enter_point['direction'] == 1:
                        bonus = key_point - last_value
                break

    return {'bonus': '' if bonus == -100000 else bonus, 'time': bonus_time,
            'max_bonus': '' if max_bonus == -100000 else max_bonus,
            'max_bonus_time': max_bonus_time, 'max_lose': '' if max_lose == -100000 else max_lose,
            'max_lose_time': max_lose_time}


def get_out_key():
    return ['date', 'base_max', 'base_min', 'break_max', 'break_min', 'direction', 'break_time', 'pre_enter',
            'key_point', 'enter_time', 'bonus', 'bonus_time', 'max_bonus', 'max_bonus_time', 'max_lose',
            'max_lose_time']
