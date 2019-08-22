from os import listdir


def list_tx1_dir(d):
    month_dir_list = list_dir(d)
    dicts = {}
    for i in range(len(month_dir_list)):
        dicts[month_dir_list[i][9:15]] = list_dir(month_dir_list[i])
    return dicts


def list_dir(d):
    dirs = sorted([d + '/' + i for i in listdir(d)])
    # dirs = sorted(dirs)
    return dirs


def get_tx1_data(f):
    data = open(f).readlines()
    data[0:1] = ()
    data1 = [i.strip('\n').strip('\r').split(',') for i in data]
    return data1
