from common import config, data_handler
from helper import raw_data_helper

# minutes
BASE_RANGE = 15
PRE_BREAK_INDEX = 10
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
    break_point = get_break_point(tx5_data, BASE_RANGE // 5, PRE_BREAK_INDEX // 5, base_point, BREAK_RANGE)

    print(base_point)

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

    for i in range(base_range):
        # print(data[i])
        min_v = int(data[i][raw_data_helper.DATA_MIN_VALUE])
        max_v = int(data[i][raw_data_helper.DATA_MAX_VALUE])
        last_v = int(data[i][raw_data_helper.DATA_LAST_VALUE])

        if (max_v > max_value) & (i >= pre_break_index) & ((last_v - max_value) >= per_break_amplitude):
            break

        if (min_v < min_value) & (i >= pre_break_index) & ((min_value - last_v) >= per_break_amplitude):
            break

        if max_v > max_value:
            max_value = max_v

        if min_v < min_value:
            min_value = min_v

    return {'max': max_value, 'min': min_value}


def get_break_point(data, base_range, pre_break_index, base_point):

    pass


def get_break_index(data, base_range, pre_break_index, baseMaxValue, baseMinValue, breakRange):
    for i in range(preBreakIndex, len(tx5Data)):
        lastValue = int(tx5Data[i][TX5_DATA_LAST_VALUE])
        if i >= breakRange:
            break
        if lastValue > baseMaxValue:
            return i
        if lastValue < baseMinValue:
            return i
    return -1


def getBreakDirection(tx5Data, preBreakIndex, baseMaxValue, baseMinValue, breakRange):
    for i in range(preBreakIndex, len(tx5Data)):
        lastValue = int(tx5Data[i][TX5_DATA_LAST_VALUE])
        if i >= breakRange:
            break
        if lastValue > baseMaxValue:
            return 0
        if lastValue < baseMinValue:
            return 1
    return -1


def writeToFile(out):
    f = open('out/out.txt', 'a')
    # print(out[(out.keys()[10])])
    baseDiff = out['baseMaxValue'] - out['baseMinValue']
    breakDiff = out['breakMaxValue'] - out['breakMinValue']
    f.write("%10s%16d%16d%16d%12d%17d%17d%13s%13d%12d%13s%16s%12d%16s%12d%16s%10d%14s\n" % (out['date'], out['diff'], out['baseMaxValue'],
                                                                                    out['baseMinValue'], baseDiff, out['breakMaxValue'], out[
        'breakMinValue'], out['breakTime'], breakDiff,
        out['keyPoint'], out['direction'], out['enterTime'], out['maxBonus'], out['maxBonusTime'],
        out['maxLoss'], out['maxLossTime'],
        out['result'], out['resultTime']))

    f.close()


def writeTitle():
    f = open('out/out.txt', 'a')
    f.write("%10s%16s%16s%16s%12s%17s%17s%13s%13s%12s%13s%16s%12s%16s%12s%16s%10s%14s\n\n" % ('date', 'diff', 'baseMaxValue', 'baseMinValue', 'baseDiff',
                                                                                      'breakMaxValue', 'breakMinValue', 'breakTime', 'breakDiff', 'keyPoint',
                                                                                      'direction', 'enterTime', 'maxBonus', 'maxBonusTime', 'maxLoss', 'maxLossTime', 'result', 'resultTime'))
    f.close()


def writeTotal():
    f = open('out/out.txt', 'a')
    global g_total
    f.write("\n\n%s\t%d\n\n" % ('total:', g_total))
    f.close()
