from helper import raw_data_helper


def get_break_point(data, pre_break_index, base_point, pre_enter_amplitude):
    break_index = -1
    direction = -1
    for i in range(pre_break_index, len(data)):
        last_value = int(data[i][raw_data_helper.DATA_LAST_VALUE])
        if last_value > int(base_point['max']):
            break_index = i
            direction = 0
            break
        if last_value < int(base_point['min']):
            break_index = i
            direction = 1
            break
    # break_index = get_break_index(data, pre_break_index, base_point)
    max_value = '' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_MAX_VALUE])
    min_value = '' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_MIN_VALUE])
    last_value = '' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_LAST_VALUE])
    time = '' if break_index == -1 else data[break_index][raw_data_helper.DATA_TIME]
    index = -1 if break_index == -1 else (break_index + 1) * 5
    diff = '' if break_index == -1 else max_value - min_value
    # pre_enter = False
    # pre_enter_point = 0
    # if break_index != -1:
    #     if (direction == 0) & (max_value - int(base_point['max']) >= pre_enter_amplitude):
    #         pre_enter_point = int(base_point['max']) + pre_enter_amplitude
    #         pre_enter = True
    #
    #     if (direction == 1) & (int(base_point['min']) - min_value >= pre_enter_amplitude):
    #         pre_enter_point = int(base_point['min']) - pre_enter_amplitude
    #         pre_enter = True

    # print(break_index)
    # return {'max': max_value, 'min': min_value, 'last': last_value, 'time': time, 'diff': diff, 'index': index,
    #         'direction': direction, 'pre_enter': pre_enter, 'pre_enter_point': pre_enter_point}

    return {'max': max_value, 'min': min_value, 'last': last_value, 'time': time, 'diff': diff, 'index': index,
            'direction': direction}
