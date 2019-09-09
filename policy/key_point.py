def get_key_point(break_point, pre_en_point, return_scale):
    key_point = -1
    direction = -1
    index = -1
    if break_point['index'] != -1:
        return_value = break_point['diff'] // return_scale
        key_point = (break_point['max'] - return_value) if break_point['direction'] == 0 else break_point[
                                                                                                  'min'] + return_value
        direction = break_point['direction']
        index = break_point['index']

    if pre_en_point['index'] != -1:
        key_point = pre_en_point['point']
        direction = pre_en_point['direction']
        index = break_point['index']

    key_point = '' if index == -1 else key_point
    direction = '' if index == -1 else direction
    return {'index': index, 'key_point': key_point, 'direction': direction}
