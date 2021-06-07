import datetime

from matplotlib.widgets import Cursor

# import raw_data_helper
import matplotlib.pyplot as plt
import mpl_finance as mpf
import numpy as np

# import pandas_datareader as pdr
from helper import raw_data_helper

K_BAR_WIDTH = 0.6
quotes = raw_data_helper.transfer(raw_data_helper.get_data("tx5_data/202002/20200214.txt"))


def draw():
    # quotes = raw_data_helper.get_data("tx5_data/202002/20200212.txt")
    start = datetime.datetime(2018, 4, 1)
    # df_2330 = pdr.DataReader('2330.TW', 'yahoo', start=start)
    # print(df_2330['Close'])
    # df_2330.index = df_2330.index.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    fig = plt.figure(figsize=(24, 8))
    # print(df_2330)
    # print(df_2330['Open'])

    ax = fig.add_subplot(1, 1, 1)
    # ax.set_xticks(range(0, len(df_2330.index), 10))
    # ax.set_xticklabels(df_2330.index[::10])
    ax.set_xticks(range(0, len(quotes["time"]), 10))
    ax.set_xticklabels(quotes["time"][::10])
    # mpf.candlestick2_ochl(ax, df_2330['Open'], df_2330['Close'], df_2330['High'],
    #                       df_2330['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
    mpf.candlestick2_ochl(ax, quotes['Open'], quotes['Close'], quotes['High'],
                          quotes['Low'], width=K_BAR_WIDTH, colorup='r', colordown='g', alpha=0.75)

    cursor = Cursor(ax, useblit=True, color='blue', linewidth=0.6)
    # cursor = Cursor(ax)
    # fig.canvas.mpl_connect('motion_notify_event', mouse_move)
    fig.align_labels()
    plt.xticks(rotation=0)

    ax.format_coord = format_coord
    plt.show()

    # fig, ax = plt.subplots(facecolor=(0.5, 0.5, 0.5))
    # fig.subplots_adjust(bottom=0.2)
    # ax.xaxis_date()
    #
    # plt.xticks(rotation=45)
    # plt.title("6158")
    # plt.xlabel("time")
    # plt.ylabel("price")
    # mpf.candlestick_ohlc(ax, quotes, width=1.2, colorup='r', colordown='green')
    # plt.grid(True)
    # plt.show()

    # quotes.index = quotes.index.format(formatter=lambda x: x.strftime('%Y-%m-%d'))
    #
    # fig = plt.figure(figsize=(24, 8))
    #
    # ax = fig.add_subplot(1, 1, 1)
    # ax.set_xticks(range(0, len(quotes.index), 10))
    # ax.set_xticklabels(quotes.index[::10])
    # mpf.candlestick2_ochl(ax, quotes['Open'], df_2330['Close'], df_2330['High'],
    #                       df_2330['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
    # plt.grid(True)
    # plt.show()


def mouse_move(event):
    print("my position:", event.button, event.xdata, event.ydata)


def format_coord(x, y):
    col = -1
    if x < 0:
        if x > -0.3:
            col = 0
    else:
        tmp = x - int(x+0.5)
        if tmp < 0.3:
            if tmp > -0.3:
                col = int(x+0.5)

    if col == -1:
        return ''
    else:
        # return 'x=%s, y=%d' % (quotes['time'][col], quotes['Close'][col])
        return 'T:%s O:%d H:%d L:%d C:%d' % (quotes['time'][col], quotes['Open'][col], quotes['High'][col], quotes['Low'][col], quotes['Close'][col])
