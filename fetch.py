from common import output, raw_data_gen, raw_data_download, config
from helper import raw_data_helper, original_data_helper
from policy import happy, pre_enter_point, max_min
from os import listdir
from datetime import datetime, timedelta

from os import listdir
import csv
import os

# output.remove()


# os.remove('out/daily.txt')
# os.remove('out/out.txt')
# os.remove('out/out2.txt')

# def listTx5Dir(tx5Dir):
#     dirList = [tx5Dir + "/" + i for i in listdir(tx5Dir)]
#     return dirList

# raw_data_download.download()
# raw_data_gen.go()

# print(listdir(config.HISTORY_TX_DIR))

# def get_history_tx_data():
#     history_tx_dir = original_data_helper.list_original_dir(config.HISTORY_TX_DIR)
#     for key in history_tx_dir:
#         if 'TXF' not in key:
#             continue
#         original_data = original_data_helper.get_data(key)
#         history_data = []
#         for i in range(0, len(original_data)):
#             print(original_data[i])
#             if original_data[i][original_data_helper.DATA_PRODUCT].strip('\n').strip(' ').strip('\r') in 'TX':
#                 history_data.append(original_data[i])
#         return history_data


# get_history_tx_data()

history_tx_data = raw_data_helper.get_data(config.HISTORY_TX_DATA)

date_list = sorted(list(set([i[0] for i in history_tx_data])))
print (date_list)

# for d in range(0, len(date_list)):
#     date_key = date_list[d].replace('/', '')
#     # print (date)
#     month_dir = date_key[0:6]
#
#     # print(month_dir)
#     original_data_helper.csv_write_header(config.HISTORY_TX1_DIR + '/' + month_dir, date_key, raw_data_gen.get_out_key())
#
#     for i in range(0, len(history_tx_data)):
#         print('date_list[d] ' + date_list[d])
#         print('history_tx_data[i][0] ' + history_tx_data[i][0])
#
#         if history_tx_data[i][0] == date_list[d]:
#             out = {'Date': history_tx_data[i][0],
#                    'Time': history_tx_data[i][1],
#                    'Open': history_tx_data[i][2],
#                    'High': history_tx_data[i][3],
#                    'Low': history_tx_data[i][4],
#                    'Close': history_tx_data[i][5],
#                    'Volume': history_tx_data[i][6],
#                    }
#
#             original_data_helper.csv_write_row(config.HISTORY_TX1_DIR + '/' + month_dir, date_key, raw_data_gen.get_out_key(), out)

# for d in range(0, len(date_list)):
#     date_key = date_list[d].replace('/', '')
#     month_dir = date_key[0:6]
#     original_data_helper.csv_write_header(config.HISTORY_TX1_DIR + '/' + month_dir, date_key,
#                                           raw_data_gen.get_out_key())

for d in range(len(date_list)):
    date_key = date_list[d].replace('/', '')
    month_dir = date_key[0:6]
    if os.path.isfile(config.HISTORY_TX1_DIR + '/' + month_dir + '/' + date_key + '.txt'):
        print('tx1 ' + date_key + ' is Exist')
        continue

    print('generate tx1 ' + date_key)
    original_data_helper.csv_write_header(config.HISTORY_TX1_DIR + '/' + month_dir, date_key,
                                          raw_data_gen.get_out_key())
    for i in range(0, len(history_tx_data)):
        if history_tx_data[i][0] == date_list[d]:
            t = int(history_tx_data[i][1].replace(':', ''))
            if (t >= 84600) & (t <= 134500):
                out = {'Date': history_tx_data[i][0],
                       'Time': history_tx_data[i][1],
                       'Open': history_tx_data[i][2],
                       'High': history_tx_data[i][3],
                       'Low': history_tx_data[i][4],
                       'Close': history_tx_data[i][5],
                       'Volume': history_tx_data[i][6],
                       }

                original_data_helper.csv_write_row(config.HISTORY_TX1_DIR + '/' + month_dir, date_key,
                                                   raw_data_gen.get_out_key(), out)

            if history_tx_data[i][1] == '13:45:00':
                break


for d in range(0, len(date_list)):
    date_key = date_list[d].replace('/', '')
    raw_data_gen.gen_history_tx5_data(date_key)

# for i in range(0, len(history_tx_data)):
#     for d in range(0, len(date_list)):
#         if history_tx_data[i][0] == date_list[d]:
#             date_key = date_list[d].replace('/', '')
#             month_dir = date_key[0:6]
#
#             if not os.path.isfile(config.HISTORY_TX1_DIR + '/' + month_dir + '/' + date_key + '.txt'):
#                 original_data_helper.csv_write_header(config.HISTORY_TX1_DIR + '/' + month_dir, date_key,
#                                                       raw_data_gen.get_out_key())
#                 first_create = True
#
#             if first_create
#
#             # print('date_list[d] ' + date_list[d])
#             # print('history_tx_data[i][0] ' + history_tx_data[i][0])
#             out = {'Date': history_tx_data[i][0],
#                    'Time': history_tx_data[i][1],
#                    'Open': history_tx_data[i][2],
#                    'High': history_tx_data[i][3],
#                    'Low': history_tx_data[i][4],
#                    'Close': history_tx_data[i][5],
#                    'Volume': history_tx_data[i][6],
#                    }
#
#             original_data_helper.csv_write_row(config.HISTORY_TX1_DIR + '/' + month_dir, date_key, raw_data_gen.get_out_key(), out)
#             break

#



# original_dir = original_data_helper.list_original_dir(config.HISTORY_TX_DIR)

# max_min.go()
# happy.go()

# pre_enter_point.go()

# print(function.getTx5Data('tx5_data/201908/20190816.txt'))

# daily_gen.go()
# alg.go()
# alg2.go()
