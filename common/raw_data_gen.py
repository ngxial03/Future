from common import config
from helper import original_data_helper
import os
from os import listdir
import datetime


def go():
    date_key = get_date_key()
    if date_key == '':
        return
    remove(date_key)
    tx_data = get_tx_data()
    nearly_data = get_nearly_tx_data(tx_data)
    morning_data = get_morning_tx_data(nearly_data)
    divide_data = divide_by_time(morning_data)
    gen_tx1_data(divide_data)
    gen_tx5_data()
    remove_original_data()


def get_date_key():
    original_dir = original_data_helper.list_original_dir(config.ORIGINAL_DIR)
    if len(original_dir) == 0:
        return ''
    original_file = ''
    for f in original_dir:
        if 'Daily_' in f:
            original_file = f
            break
    if original_file == '':
        return ''
    date = original_file[20:30].split('_')
    return date[0] + date[1] + date[2]


def get_tx_data():
    original_dir = original_data_helper.list_original_dir(config.ORIGINAL_DIR)
    for key in original_dir:
        if 'Daily_' not in key:
            continue
        original_data = original_data_helper.get_data(key)
        tx_data = []
        for i in range(0, len(original_data)):
            # print(original_data[i])
            if original_data[i][original_data_helper.DATA_PRODUCT].strip('\n').strip(' ').strip('\r') in 'TX':
                tx_data.append(original_data[i])
        return tx_data


def get_nearly_tx_data(tx_data):
    date_list = sorted(list(set([i[2] for i in tx_data])))
    # print(date_list)
    # data2 = {}
    # for date in date_list:
    #     data2[date] = [i for i in tx_data if i[2] == date]
    data = [i for i in tx_data if i[2] == date_list[0]]
    return data


def get_morning_tx_data(tx_data):
    key = get_date_key()
    data = []
    for i in tx_data:
        if (i[0] in key) & (i[3] >= '084500') & (i[3] <= '134459'):
            data.append(i)
    return data


def divide_by_time(data):
    time_list = sorted(list(set([i[3][0:4] for i in data])))
    data2 = {}
    for time in time_list:
        data2[time] = [i for i in data if i[3][0:4] == time]
    return data2


def gen_tx1_data(divide_data):
    # print(divide_data)
    date_key = get_date_key()
    date = date_key[0:4] + '/' + date_key[4:6] + '/' + date_key[6:8]
    month_dir = date_key[0:6]
    original_data_helper.csv_write_header(config.TX1_DIR + '/' + month_dir, date_key, get_out_key())
    for time_key in sorted(divide_data.keys()):
        # print(time_key)
        # print(time_key)
        data = divide_data[time_key]
        open_v = int(data[0][4])
        close = int(data[len(data) - 1][4])
        high = 0
        low = 100000000
        volume = 0

        for d in data:
            if int(d[4]) > high:
                high = int(d[4])
            if int(d[4]) < low:
                low = int(d[4])
            volume = volume + int((int(d[5]) / 2))

        t = datetime.datetime.strptime(time_key, "%H%M") + datetime.timedelta(minutes=1)
        # t = t.timedelta(minutes=1)
        time = t.strftime("%H:%M:%S")
        # time = time_key[0:2] + ':' + ("%02d" % (int(time_key[2:4]) + 1)) + ':00'
        # time = time[0:2] + ':' + time[2:4] + ':00'
        # print('date ' + date)
        # print(open)
        # print(high)
        # print(low)
        # print(close)
        # print(volume)
        out = {'Date': date,
               'Time': time,
               'Open': open_v,
               'High': high,
               'Low': low,
               'Close': close,
               'Volume': volume
               }

        original_data_helper.csv_write_row(config.TX1_DIR + '/' + month_dir, date_key, get_out_key(), out)


def gen_tx5_data():
    date_key = get_date_key()
    month_dir = date_key[0:6]
    tx1_data = original_data_helper.get_data(config.TX1_DIR + '/' + month_dir + '/' + date_key + '.txt')
    original_data_helper.csv_write_header(config.TX5_DIR + '/' + month_dir, date_key, get_out_key())

    open_v = 0
    high = 0
    low = 100000000
    volume = 0

    tx1_data[0:1] = ()
    # print(tx1_data)
    for i in range(len(tx1_data)):
        if i % 5 == 0:
            open_v = tx1_data[i][2]
            high = 0
            low = 100000000
            volume = 0

        if int(tx1_data[i][3]) > high:
            high = int(tx1_data[i][3])
        if int(tx1_data[i][4]) < low:
            low = int(tx1_data[i][4])
        volume = volume + int(tx1_data[i][6])

        if i % 5 == 4:
            out = {'Date': tx1_data[i][0],
                   'Time': tx1_data[i][1],
                   'Open': open_v,
                   'High': high,
                   'Low': low,
                   'Close': tx1_data[i][5],
                   'Volume': volume
                   }

            original_data_helper.csv_write_row(config.TX5_DIR + '/' + month_dir, date_key, get_out_key(), out)

    # print(tx1_data)


def gen_history_tx5_data(date_key):
    # date_key = get_date_key()
    month_dir = date_key[0:6]
    if os.path.isfile(config.HISTORY_TX5_DIR + '/' + month_dir + '/' + date_key + '.txt'):
        return

    tx1_data = original_data_helper.get_data(config.HISTORY_TX1_DIR + '/' + month_dir + '/' + date_key + '.txt')
    original_data_helper.csv_write_header(config.HISTORY_TX5_DIR + '/' + month_dir, date_key, get_out_key())

    open_v = 0
    high = 0
    low = 100000000
    volume = 0

    tx1_data[0:1] = ()
    # print(tx1_data)
    for i in range(len(tx1_data)):
        if i % 5 == 0:
            open_v = tx1_data[i][2]
            high = 0
            low = 100000000
            volume = 0

        if int(tx1_data[i][3]) > high:
            high = int(tx1_data[i][3])
        if int(tx1_data[i][4]) < low:
            low = int(tx1_data[i][4])
        volume = volume + int(tx1_data[i][6])

        if i % 5 == 4:
            out = {'Date': tx1_data[i][0],
                   'Time': tx1_data[i][1],
                   'Open': open_v,
                   'High': high,
                   'Low': low,
                   'Close': tx1_data[i][5],
                   'Volume': volume
                   }

            original_data_helper.csv_write_row(config.HISTORY_TX5_DIR + '/' + month_dir, date_key, get_out_key(), out)

    # print(tx1_data)


def get_out_key():
    return ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']


def remove(date_key):
    # print(date_key)
    month_dir = date_key[0:6]
    # print(dir)
    tx1_out = config.TX1_DIR + '/' + month_dir + '/' + date_key + '.txt'
    tx5_out = config.TX5_DIR + '/' + month_dir + '/' + date_key + '.txt'
    # print(tx5_out)
    if os.path.isfile(tx1_out):
        os.remove(tx1_out)
    if os.path.isfile(tx5_out):
        os.remove(tx5_out)


def remove_original_data():
    # files = [config.ORIGINAL_DIR + '/' + i for i in listdir(config.ORIGINAL_DIR + '/') if 'Daily_' not in i]
    files = [config.ORIGINAL_DIR + '/' + i for i in listdir(config.ORIGINAL_DIR + '/')]
    # print(files)
    for f in range(len(files)):
        os.remove(files[f])
