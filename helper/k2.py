import pandas as pd
import matplotlib
import mplfinance as mpf


# 導入pandas、matplotlib、mplfinance模組，將mplfinance模組縮寫為mpf
# 這邊要導入matplotlib的原因是因為mplfinance繪圖時需要調用mptplotlib模組


def draw(date):
    # target_stock = '0050' #設定要繪製走勢圖的股票
    # df = pd.read_csv(f'./data/{target_stock}.csv', parse_dates=True, index_col=1) #讀取目標股票csv檔的位置

    d = date[:6]
    # print(dir)
    df = pd.read_csv('tx5_data/' + d + '/' + date + '.txt')
    print(df)
    df.index = pd.DatetimeIndex(df['Time'])

    # df.rename(columns={'Time': 'dates'}, inplace=True)
    # df.rename(columns={'Open': 'opens'}, inplace=True)
    # df.rename(columns={'High': 'highs'}, inplace=True)
    # df.rename(columns={'Low': 'lows'}, inplace=True)
    # df.rename(columns={'Close': 'closes'}, inplace=True)
    # df.rename(columns={'Volume': 'volumes'}, inplace=True)

    # print(df)

    # 這裡針對資料表做一下修正，因為交易量(Turnover)在mplfinance中須被改為Volume才能被認出來

    mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
    s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
    # 針對線圖的外觀微調，將上漲設定為紅色，下跌設定為綠色，符合台股表示習慣
    # 接著把自訂的marketcolors放到自訂的style中，而這個改動是基於預設的yahoo外觀

    kwargs = dict(type='candle', mav=(5, 10, 20), volume=True, figratio=(10, 5), figscale=1, title=date, style=s)
    # 設定可變參數kwargs，並在變數中填上繪圖時會用到的設定值

    mpf.plot(df, **kwargs)
    # 選擇df資料表為資料來源，帶入kwargs參數，畫出目標股票的走勢圖
