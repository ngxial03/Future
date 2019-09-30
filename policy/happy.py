from common import config, data_handler
from helper import raw_data_helper
from policy import base_point, break_point, pre_enter_point, key_point, enter_point, bonus_point
import csv

# minutes
BASE_RANGE = 15  # 09:00:00
PRE_BREAK_INDEX = 10  # 08:55:00
BREAK_RANGE = 75  # 10:00:00
TERMINAL_TIME = 120  # 10:45:00

# points
PRE_BREAK_AMPLITUDE = 5
PRE_ENTER_AMPLITUDE = 5
PRE_BONUS_AMPLITUDE = 17
WIN_AMPLITUDE = 31
LOSE_AMPLITUDE = 28

# const
RETURN_SCALE = 3

# global
total_bonus = 0
month_bonus = 0


def go():
    # writeTitle()

    tx1_dir = raw_data_helper.list_raw_dir(config.TX1_DIR)
    tx5_dir = raw_data_helper.list_raw_dir(config.TX5_DIR)
    # print(tx5_dir)

    raw_data_helper.csv_write_header('happy_total', get_out_key())

    for key in sorted(tx1_dir.keys()):
        # print (key)
        # print (tx1_helper.get_tx1_data(tx1_dir[key][0]))
        raw_data_helper.csv_write_header('happy_' + key, get_out_key())

        for p in range(len(tx1_dir[key])):
            # if '201908' not in key:
            #     break
            trace(key, tx1_dir[key][p], tx5_dir[key][p])
            # break
        # break
        global month_bonus
        print(month_bonus)
        month_bonus = 0

    global total_bonus
    print('--------------')
    print(total_bonus)


def trace(month, tx1_file, tx5_file):
    # print(tx1_file)
    # print(tx5_file)

    # dailyData = function2.getDailyData(config.TX_DAILY_DIR)
    tx1_data = raw_data_helper.get_data(tx1_file)
    tx5_data = raw_data_helper.get_data(tx5_file)

    b_point = base_point.get_base_point(tx5_data, BASE_RANGE // 5, PRE_BREAK_INDEX // 5, PRE_BREAK_AMPLITUDE)
    # print(b_point)

    brk_point = break_point.get_break_point(tx5_data, PRE_BREAK_INDEX // 5, b_point, RETURN_SCALE)
    # print(brk_point)

    pre_en_point = pre_enter_point.get_pre_enter_point(tx1_data, PRE_BREAK_INDEX, b_point, PRE_ENTER_AMPLITUDE)

    k_point = key_point.get_key_point(brk_point, pre_en_point, RETURN_SCALE)
    # print(k_point)

    en_point = enter_point.get_enter_point(tx1_data, k_point, BREAK_RANGE)
    # print(enter_point)

    bon_point = bonus_point.get_bonus_point(tx1_data, en_point['enter_point'], en_point['direction'], en_point['index'],
                                            TERMINAL_TIME, PRE_BONUS_AMPLITUDE,
                                            WIN_AMPLITUDE,
                                            LOSE_AMPLITUDE)
    # print(bonus_point)
    global month_bonus
    global total_bonus
    if bon_point['bonus'] != '':
        month_bonus = month_bonus + int(bon_point['bonus'])
        total_bonus = total_bonus + int(bon_point['bonus'])

    # print(tx1_data[0])
    out = {'date': tx1_data[0][data_handler.DATA_DATE],
           'base_max': b_point['max'],
           'base_min': b_point['min'],
           'break_max': brk_point['max'],
           'break_min': brk_point['min'],
           'break_direction': 'up' if brk_point['direction'] == 0 else ('down' if brk_point['direction'] == 1 else ''),
           'break_time': brk_point['time'],
           'break_key_point': brk_point['break_key_point'],
           'pre_enter_direction': 'up' if pre_en_point['direction'] == 0 else (
               'down' if pre_en_point['direction'] == 1 else ''),
           'pre_enter_time': pre_en_point['time'],
           'pre_enter': '' if pre_en_point['index'] == -1 else pre_en_point['pre_enter_point'],
           'enter_direction': 'up' if en_point['direction'] == 0 else ('down' if en_point['direction'] == 1 else ''),
           'enter_time': en_point['time'],
           'enter_point': en_point['enter_point'],
           'bonus': bon_point['bonus'],
           'bonus_time': bon_point['time'],
           'max_bonus': bon_point['max_bonus'],
           'max_bonus_time': bon_point['max_bonus_time'],
           'max_lose': bon_point['max_lose'],
           'max_lose_time': bon_point['max_lose_time']}

    # print('\n')

    raw_data_helper.csv_write_row('happy_' + month, get_out_key(), out)
    raw_data_helper.csv_write_row('happy_total', get_out_key(), out)


def get_out_key():
    return ['date', 'base_max', 'base_min', 'break_max', 'break_min', 'break_direction', 'break_time',
            'break_key_point', 'pre_enter_direction', 'pre_enter_time', 'pre_enter', 'enter_direction',
            'enter_time', 'enter_point', 'bonus', 'bonus_time', 'max_bonus', 'max_bonus_time', 'max_lose',
            'max_lose_time']
