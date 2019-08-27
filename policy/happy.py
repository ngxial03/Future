from common import config, data_handler
from helper import raw_data_helper

# minutes
BASE_RANGE = 15  # 09:00:00
PRE_BREAK_INDEX = 10  # 08:55:00
BREAK_RANGE = 75  # 10:00:00
TERMINAL_TIME = 165  # 11:30:00

# points
PRE_BREAK_AMPLITUDE = 5
BREAK_AMPLITUDE = 12
WIN_AMPLITUDE = 26
LOSE_AMPLITUDE = 26

# const
RETURN_SCALE = 3


def go():
    writeTitle()

    tx1_dir = raw_data_helper.list_raw_dir(config.TX1_DIR)
    tx5_dir = raw_data_helper.list_raw_dir(config.TX5_DIR)
    # print(tx5_dir)

    for key in tx1_dir:
        print (key)
        # print (tx1_helper.get_tx1_data(tx1_dir[key][0]))
        for p in range(len(tx1_dir[key])):
            trace(tx1_dir[key][p], tx5_dir[key][p])
            # break
        break


def trace(tx1_file, tx5_file):
    # print(tx1_file)
    # print(tx5_file)

    # dailyData = function2.getDailyData(config.TX_DAILY_DIR)
    tx1_data = raw_data_helper.get_data(tx1_file)
    tx5_data = raw_data_helper.get_data(tx5_file)

    base_point = get_base_point(tx5_data, BASE_RANGE // 5, PRE_BREAK_INDEX // 5, PRE_BREAK_AMPLITUDE)
    # print(base_point)

    break_point = get_break_point(tx5_data, PRE_BREAK_INDEX // 5, base_point)
    # print(break_point)

    key_point = get_key_point(break_point, RETURN_SCALE)
    # print(key_point)

    enter_point = get_enter_point(tx1_data, break_point, key_point)
    # print(enter_point)

    result_point = get_result_point(tx1_data, enter_point, key_point, TERMINAL_TIME, WIN_AMPLITUDE, LOSE_AMPLITUDE)
    print(result_point)

    # baseMinValue = function.getBaseMinValue(
    #     tx5Data, BASE_RANGE, PRE_BREAK_INDEX, PRE_BREAK_AMPLITUDE)
    #
    # out = {}
    # diff = function2.getDiff(dailyData, tx5Data[0][function.TX5_DATA_DATE])
    # out['diff'] = diff
    #
    # out['baseMaxValue'] = baseMaxValue
    # out['baseMinValue'] = baseMinValue
    #
    # breakIndex = function.getBreakIndex(
    #     tx5Data, PRE_BREAK_INDEX, baseMaxValue, baseMinValue, BREAK_RANGE)
    #
    # direction = function.getBreakDirection(
    #     tx5Data, PRE_BREAK_INDEX, baseMaxValue, baseMinValue, BREAK_RANGE)
    #
    # out['date'] = tx5Data[0][function.TX5_DATA_DATE]
    # if breakIndex >= 0 & direction >= 0:
    #     out['direction'] = ("up", "down")[direction == 1]
    #     out['breakMaxValue'] = int(
    #         tx5Data[breakIndex][function.TX5_DATA_MAX_VALUE])
    #     out['breakMinValue'] = int(
    #         tx5Data[breakIndex][function.TX5_DATA_MIN_VALUE])
    #     out['breakTime'] = tx5Data[breakIndex][function.TX5_DATA_TIME]
    #
    #     keyPoint = function.getKeyPoint(
    #         tx5Data, breakIndex, direction, RETURN_SCALE)
    #     out['keyPoint'] = keyPoint
    #
    #     enterTime = function.getEnterTime(tx5Data, breakIndex, direction, keyPoint)
    #     out['enterTime'] = enterTime
    #
    #     result = function.getResult(
    #         tx5Data, breakIndex, direction, keyPoint, TERMINAL_TIME, WIN_AMPLITUDE, LOSE_AMPLITUDE)
    #     out['result'] = result['bonus']
    #     out['resultTime'] = result['touchTime']
    #
    #     maxBonus = function.getMaxBonus(
    #         tx5Data, breakIndex, direction, keyPoint, TERMINAL_TIME)
    #     out['maxBonus'] = maxBonus['maxBonus']
    #     out['maxBonusTime'] = maxBonus['time']
    #
    #     maxLoss = function.getMaxLoss(
    #         tx5Data, breakIndex, direction, keyPoint, out['resultTime'])
    #     out['maxLoss'] = maxLoss['maxLoss']
    #     out['maxLossTime'] = maxLoss['time']
    # else:
    #     out['direction'] = "-"
    #     out['breakMaxValue'] = 0
    #     out['breakMinValue'] = 0
    #     out['breakTime'] = '00:00:00'
    #     out['keyPoint'] = 0
    #     out['enterTime'] = 0
    #     out['maxBonus'] = 0
    #     out['maxBonusTime'] = '00:00:00'
    #     out['maxLoss'] = 0
    #     out['maxLossTime'] = '00:00:00'
    #     out['result'] = 0
    #     out['resultTime'] = '00:00:00'
    #
    # global g_total
    # g_total = g_total + out['result']
    # writeToFile(out)


def get_base_point(data, base_range, pre_break_index, per_break_amplitude):
    max_value = 0
    min_value = 1000000
    pre_break = False

    for i in range(base_range):
        # print(data[i])
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


def get_break_point(data, pre_break_index, base_point):
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
    max_value = '-1' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_MAX_VALUE])
    min_value = '-1' if break_index == -1 else int(data[break_index][raw_data_helper.DATA_MIN_VALUE])
    time = '-1' if break_index == -1 else data[break_index][raw_data_helper.DATA_TIME]
    index = '-1' if break_index == -1 else (break_index + 1) * 5

    # print(break_index)
    return {'max': max_value, 'min': min_value, 'time': time, 'diff': max_value - min_value, 'index': index,
            'direction': direction}


def get_key_point(break_point, return_scale):
    key_point = -1
    if break_point['index'] != -1:
        return_value = break_point['diff'] // return_scale
        key_point = (break_point['max'] - return_value) if break_point['direction'] == 0 else break_point[
                                                                                                  'min'] + return_value
    return key_point


def get_enter_point(data, break_point, key_point):
    index = -1
    if break_point['index'] != -1:
        for i in range(break_point['index'], len(data)):
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

    max_value = '-1' if break_point['index'] == -1 else int(data[index][raw_data_helper.DATA_MAX_VALUE])
    min_value = '-1' if break_point['index'] == -1 else int(data[index][raw_data_helper.DATA_MIN_VALUE])
    time = '-1' if break_point['index'] == -1 else data[index][raw_data_helper.DATA_TIME]
    return {'max': max_value, 'min': min_value, 'time': time, 'index': index + 1, 'direction': break_point['direction']}


def get_result_point(data, enter_point, key_point, terminal_time, win_amplitude, lose_amplitude):
    bonus = 0
    touch_time = '00:00:00'

    for i in range(enter_point['index'], len(data)):
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

        if win >= win_amplitude:
            bonus = win_amplitude
            touch_time = time
            break

        if lose >= lose_amplitude:
            bonus = -1 * lose_amplitude
            touch_time = time
            break

        if i >= terminal_time - 1:
            touch_time = time
            if enter_point['direction'] == 0:
                bonus = last_value - key_point
            if enter_point['direction'] == 1:
                bonus = key_point - last_value
            break

    return {'bonus': bonus, 'time': touch_time}


def writeToFile(out):
    f = open('out/out.txt', 'a')
    # print(out[(out.keys()[10])])
    baseDiff = out['baseMaxValue'] - out['baseMinValue']
    breakDiff = out['breakMaxValue'] - out['breakMinValue']
    f.write("%10s%16d%16d%16d%12d%17d%17d%13s%13d%12d%13s%16s%12d%16s%12d%16s%10d%14s\n" % (
        out['date'], out['diff'], out['baseMaxValue'],
        out['baseMinValue'], baseDiff, out['breakMaxValue'], out[
            'breakMinValue'], out['breakTime'], breakDiff,
        out['keyPoint'], out['direction'], out['enterTime'], out['maxBonus'], out['maxBonusTime'],
        out['maxLoss'], out['maxLossTime'],
        out['result'], out['resultTime']))

    f.close()


def writeTitle():
    f = open('out/out.txt', 'a')
    f.write("%10s%16s%16s%16s%12s%17s%17s%13s%13s%12s%13s%16s%12s%16s%12s%16s%10s%14s\n\n" % (
        'date', 'diff', 'baseMaxValue', 'baseMinValue', 'baseDiff',
        'breakMaxValue', 'breakMinValue', 'breakTime', 'breakDiff', 'keyPoint',
        'direction', 'enterTime', 'maxBonus', 'maxBonusTime', 'maxLoss', 'maxLossTime', 'result', 'resultTime'))
    f.close()


def writeTotal():
    f = open('out/out.txt', 'a')
    global g_total
    f.write("\n\n%s\t%d\n\n" % ('total:', g_total))
    f.close()
