def get_daily_data(file):
    data = open(
        file).readlines()
    data[0:1] = ()
    data1 = [i.strip('\n').strip('\r').split(',') for i in data]
    return data1
