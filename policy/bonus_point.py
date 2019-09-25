from helper import raw_data_helper


def get_bonus_point(tx1_data, point, direction, start_diff_time, end_diff_time, pre_bonus_amplitude, win_amplitude,
                    lose_amplitude):
    bonus = -100000
    bonus_time = ''
    max_bonus = 0
    max_bonus_time = ''
    max_lose = 0
    max_lose_time = ''

    if start_diff_time != -1:
        for i in range(start_diff_time - 1, len(tx1_data)):
            max_value = int(tx1_data[i][raw_data_helper.DATA_MAX_VALUE])
            min_value = int(tx1_data[i][raw_data_helper.DATA_MIN_VALUE])
            last_value = int(tx1_data[i][raw_data_helper.DATA_LAST_VALUE])
            time = tx1_data[i][raw_data_helper.DATA_TIME]
            win = 0
            lose = 0

            if direction == 0:
                lose = point - min_value
                win = max_value - point

            if direction == 1:
                lose = max_value - point
                win = point - min_value

            if win > max_bonus:
                max_bonus = win
                max_bonus_time = time

            if lose > max_lose:
                max_lose = lose
                max_lose_time = time

            if (lose > 0) & (max_bonus >= pre_bonus_amplitude) & (bonus == -100000):
                bonus = 0
                bonus_time = time
                break

            if (win >= win_amplitude) & (bonus == -100000):
                bonus = win_amplitude
                bonus_time = time
                # break

            if (lose >= lose_amplitude) & (bonus == -100000):
                bonus = -1 * lose_amplitude
                bonus_time = time
                # break

            if i >= end_diff_time - 1:
                if bonus == -100000:
                    bonus_time = time
                    if direction == 0:
                        bonus = last_value - point
                    if direction == 1:
                        bonus = point - last_value
                break

    return {'bonus': '' if bonus == -100000 else bonus, 'time': bonus_time,
            'max_bonus': '' if bonus == -100000 else max_bonus, 'max_bonus_time': max_bonus_time,
            'max_lose': '' if bonus == -100000 else max_lose, 'max_lose_time': max_lose_time}
