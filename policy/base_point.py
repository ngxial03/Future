from helper import raw_data_helper


def get_base_point(data, base_range, pre_break_index, per_break_amplitude):
    max_value = 0
    min_value = 1000000
    pre_break = False

    for i in range(base_range):
        min_v = int(data[i][raw_data_helper.DATA_MIN_VALUE])
        max_v = int(data[i][raw_data_helper.DATA_MAX_VALUE])
        last_v = int(data[i][raw_data_helper.DATA_LAST_VALUE])

        if (max_v > max_value) & (i >= pre_break_index) & ((last_v - max_value) >= per_break_amplitude):
            pre_break = True
            break

        if (min_v < min_value) & (i >= pre_break_index) & ((min_value - last_v) >= per_break_amplitude):
            pre_break = True
            break

        if max_v > max_value:
            max_value = max_v

        if min_v < min_value:
            min_value = min_v

    index = 15 if pre_break else 10
    return {'max': max_value, 'min': min_value, 'pre_break': pre_break, 'diff': max_value - min_value, 'index': index}