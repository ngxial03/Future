from helper import raw_data_helper


def get_bonus_point(data, enter_point, key_point, terminal_time, pre_bonus_amplitude, win_amplitude, lose_amplitude):
    bonus = -100000
    bonus_time = ''
    max_bonus = -100000
    max_bonus_time = ''
    max_lose = -100000
    max_lose_time = ''

    if enter_point['index'] != -1:
        # print(enter_point['index'])
        for i in range(enter_point['index'] - 1, len(data)):
            time = data[i][raw_data_helper.DATA_TIME]
            max_value = int(data[i][raw_data_helper.DATA_MAX_VALUE])
            min_value = int(data[i][raw_data_helper.DATA_MIN_VALUE])
            last_value = int(data[i][raw_data_helper.DATA_LAST_VALUE])
            win = 0
            lose = 0

            if enter_point['direction'] == 0:
                lose = key_point - min_value
                win = max_value - key_point

            if enter_point['direction'] == 1:
                lose = max_value - key_point
                win = key_point - min_value

            if win > max_bonus:
                max_bonus = win
                max_bonus_time = time

            if lose > max_lose:
                max_lose = lose
                max_lose_time = time

            if (lose > 0) & (max_bonus >= pre_bonus_amplitude):
                bonus = 1
                bonus_time = time
                break

            if (win >= win_amplitude) & (bonus == -100000):
                bonus = win_amplitude
                bonus_time = time
                break

            if (lose >= lose_amplitude) & (bonus == -100000):
                bonus = -1 * lose_amplitude
                bonus_time = time
                break

            if i >= terminal_time - 1:
                if bonus == -100000:
                    bonus_time = time
                    if enter_point['direction'] == 0:
                        bonus = last_value - key_point
                    if enter_point['direction'] == 1:
                        bonus = key_point - last_value
                break

    return {'bonus': '' if bonus == -100000 else bonus, 'time': bonus_time,
            'max_bonus': '' if max_bonus == -100000 else max_bonus,
            'max_bonus_time': max_bonus_time, 'max_lose': '' if max_lose == -100000 else max_lose,
            'max_lose_time': max_lose_time}