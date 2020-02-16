import datetime

import raw_data_helper
import matplotlib.pyplot as plt
import mpl_finance as mpf
import pandas_datareader as pdr


def draw():
    quotes = raw_data_helper.transfer(raw_data_helper.get_data("tx5_data/202002/20200212.txt"))
    # quotes = raw_data_helper.get_data("tx5_data/202002/20200212.txt")
    print(quotes)

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
    ax.set_xticks(range(0, len(quotes["time"]), 1))
    ax.set_xticklabels(quotes["time"][::1])
    # mpf.candlestick2_ochl(ax, df_2330['Open'], df_2330['Close'], df_2330['High'],
    #                       df_2330['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
    mpf.candlestick2_ochl(ax, quotes['Open'], quotes['Close'], quotes['High'],
                          quotes['Low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
    plt.xticks(rotation=90)
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
