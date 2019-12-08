def get_key_point(break_point, pre_en_point, return_scale):
    key_point = -1
    direction = -1
    index = -1
    is_pre_enter = False
    if break_point['index'] != -1:
        return_value = break_point['diff'] // return_scale
        key_point = (break_point['max'] - return_value) if break_point['direction'] == 0 else break_point[
                                                                                                  'min'] + return_value
        direction = break_point['direction']
        index = break_point['index']

    if ((pre_en_point['index'] != -1) & (break_point['index'] == -1)) or \
            ((pre_en_point['index'] != -1) & (break_point['index'] != -1) & (
                    pre_en_point['index'] <= break_point['index'])):
        key_point = pre_en_point['pre_enter_point']
        direction = pre_en_point['direction']
        index = pre_en_point['index']
        is_pre_enter = True

    # if (pre_en_point['index'] != -1) & (break_point['index'] != -1) & (pre_en_point['index'] <= break_point['index']):
    # if break_point['index'] - pre_en_point['index'] <= 1:
    #     key_point = pre_en_point['pre_enter_point']
    #     direction = pre_en_point['direction']
    #     index = pre_en_point['index']
    #     is_pre_enter = True
    # else:
    #     return_value = break_point['diff'] // return_scale
    #     key_point = (break_point['max'] - return_value) if break_point['direction'] == 0 else break_point[
    #                                                                                               'min'] + return_value
    #     direction = break_point['direction']
    #     index = break_point['index']

    key_point = '' if index == -1 else key_point
    direction = '' if index == -1 else direction
    return {'index': index, 'key_point': key_point, 'direction': direction, 'is_pre_enter': is_pre_enter}
