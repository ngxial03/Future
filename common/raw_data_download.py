from common import config
# from urllib.request import urlopen
# from urllib2 import urlopen
import urllib.request
import zipfile
import os
import datetime


def download():
    print('download')
    today = datetime.date.today().strftime("%Y_%m_%d")
    # today = '2021_07_20'
    file_name = 'Daily_'+today+'.zip'
    tx_dir_name = datetime.date.today().strftime("%Y%m")
    tx_file_name = datetime.date.today().strftime("%Y%m%d") + '.txt'
    week_day = datetime.date.today().weekday()
    hour = datetime.datetime.now().hour
    # file_name = 'Daily_'+'2021_07_20'+'.zip'

    if week_day == 5 or week_day == 6:
        return

    if hour < 15:
        return

    print('download : ' + file_name)


    if os.path.isfile(config.TX1_DIR + '/'+tx_dir_name+'/' + tx_file_name) \
            and os.path.isfile(config.TX5_DIR + '/'+tx_dir_name+'/' + tx_file_name):
        return
    # download_url = urlopen('https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/'+file_name)
    # print('https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/'+file_name)
    # zip_content = download_url.read()

    zip_content = urllib.request.urlopen('https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/'+file_name).read()

    with open(config.ORIGINAL_DIR + '/' + file_name, 'wb') as f:
        f.write(zip_content)

    try:
        with zipfile.ZipFile(open(config.ORIGINAL_DIR + '/' +file_name, 'rb')) as f:
            f.extractall(config.ORIGINAL_DIR)
    except:
        print('sf')

    if os.path.isfile(config.ORIGINAL_DIR + '/' + file_name):
        os.remove(config.ORIGINAL_DIR + '/' + file_name)
