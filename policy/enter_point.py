from helper import raw_data_helper


def get_enter_point(data,key_point, break_range):
    index = -1
    # print(break_point['index'])
    if (key_point['index'] != -1) & (key_point['index'] < break_range):
        r = key_point['index']
        if key_point['pre_enter']:
            r = r - 5

        for i in range(r, len(data)):
            if break_point['direction'] == 0:
                min_v = int(data[i][raw_data_helper.DATA_MIN_VALUE])
                if min_v <= key_point:
                    index = i
                    break
            if break_point['direction'] == 1:
                max_v = int(data[i][raw_data_helper.DATA_MAX_VALUE])
                if max_v >= key_point:
                    index = i
                    break

    # print(index)
    max_value = '' if (index == -1) | (break_point['index'] == -1) | (break_point['index'] >= break_range) else int(
        data[index][raw_data_helper.DATA_MAX_VALUE])
    min_value = '' if (index == -1) | (break_point['index'] == -1) | (break_point['index'] >= break_range) else int(
        data[index][raw_data_helper.DATA_MIN_VALUE])
    time = '' if (index == -1) | (break_point['index'] == -1) | (break_point['index'] >= break_range) else data[index][
        raw_data_helper.DATA_TIME]
    index = -1 if index == -1 else index + 1
    return {'max': max_value, 'min': min_value, 'time': time, 'index': index, 'direction': break_point['direction']}