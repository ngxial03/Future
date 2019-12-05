from common import config
from urllib.request import urlopen
import zipfile
import os
import datetime

def download():
    today =  datetime.date.today().strftime("%Y_%m_%d")
    file_name = 'Daily_'+today+'.zip'
    tx_dir_name = datetime.date.today().strftime("%Y%m")
    tx_file_name = datetime.date.today().strftime("%Y%m%d") + '.txt'

    if os.path.isfile(config.TX1_DIR + '/'+tx_dir_name+'/' + tx_file_name) \
            and os.path.isfile(config.TX5_DIR + '/'+tx_dir_name+'/' + tx_file_name):
        return

    print ("下載前30個交易日期貨每筆成交資料...")
    download_url = urlopen('https://www.taifex.com.tw/file/taifex/Dailydownload/DailydownloadCSV/'+file_name)
    zip_content = download_url.read()
    with open(config.ORIGINAL_DIR + '/' + file_name, 'wb') as f:
        f.write(zip_content)

    print ("資料解壓縮...")
    with zipfile.ZipFile(open(config.ORIGINAL_DIR + '/' +file_name, 'rb')) as f:
        f.extractall(config.ORIGINAL_DIR)

    print ("解壓縮完成!")

    if os.path.isfile(config.ORIGINAL_DIR + '/' + file_name):
        os.remove(config.ORIGINAL_DIR + '/' + file_name)