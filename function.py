# 取出成交資料	
def GetMatchData():
    # 開啟檔案並讀檔
    data = open('C:/Users/Edward_Wu/Desktop/Future/tx15_data/20190529.txt').readlines()
    # 刪除每行的換行符號，並將資料依逗點分隔
    data1 = [ i.strip('\n').split(',') for i in data ]
    # 取出可供回測的日期清單
    date_list = sorted(list(set([ i[1] for i in data1 ])))
    # 將所有資料依日期分類
    data2={}
    for date in date_list:
     data2[date]=[ i for i in data1 if i[1]==date ]
    return data2