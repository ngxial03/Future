def get_key_point(break_point, return_scale):
    key_point = -1
    if break_point['index'] != -1:
        return_value = break_point['diff'] // return_scale
        key_point = (break_point['max'] - return_value) if break_point['direction'] == 0 else break_point[
                                                                                                  'min'] + return_value
    if break_point['pre_enter']:
        key_point = break_point['pre_enter_point']
    return '' if key_point == -1 else key_point
