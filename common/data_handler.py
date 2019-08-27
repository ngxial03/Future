DATA_DATE = 0
DATA_TIME = 1
DATA_OPEN_VALUE = 2
DATA_MAX_VALUE = 3
DATA_MIN_VALUE = 4
DATA_LAST_VALUE = 5
DATA_VOLUME = 6





# def get_base_range(data, base_range, pre_break_index, per_break_amplitude):
#     max_value = 0
#     min_value = 1000000
#     for i in range(base_range):
#         min_v = int(data[i][DATA_MIN_VALUE])
#         max_v = int(data[i][DATA_MAX_VALUE])
#         last_v = int(data[i][DATA_LAST_VALUE])
#         if max_v > max_value:
#             if (i < pre_break_index) | ((last_v - max_v) < per_break_amplitude):
#                 max_value = max_v
#         if min_v < min_value:
#             if (i < pre_break_index) | ((min_value - last_v) < per_break_amplitude):
#                 min_value = min_v
#
#     return {'max': max_value, 'min': min_value}


def getBreakIndex(tx5Data, preBreakIndex, baseMaxValue, baseMinValue, breakRange):
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


def getKeyPoint(tx5Data, breakIndex, direction, returnScale):
    keyPoint = -1
    if breakIndex > 0:
        breakPoint = tx5Data[breakIndex]
        breakMaxValue = int(breakPoint[TX5_DATA_MAX_VALUE])
        breakMinValue = int(breakPoint[TX5_DATA_MIN_VALUE])
        diff = breakMaxValue - breakMinValue
        returnValue = diff / returnScale
        keyPoint = (breakMinValue + returnValue,
                    breakMaxValue - returnValue)[direction == 0]

    return keyPoint

def getEnterTime(tx5Data, breakIndex, direction, keyPoint):
    time = -1
    if breakIndex > 0:
        for i in range(breakIndex+1, len(tx5Data)):
            if direction == 0:
                minValue = int(tx5Data[i][TX5_DATA_MIN_VALUE])
                if minValue <= keyPoint:
                    time = tx5Data[i][TX5_DATA_TIME]
                    break
            if direction == 1:
                maxValue = int(tx5Data[i][TX5_DATA_MAX_VALUE])
                if maxValue >= keyPoint:
                    time = tx5Data[i][TX5_DATA_TIME]
                    break
    return time

def getResult(tx5Data, breakIndex, direction, keyPoint, terminalTime, winAmplitude, loseAmplitude):
    result = {}
    bonus = 0
    touchTime = '00:00:00'

    for i in range(breakIndex+1, len(tx5Data)):
        time = tx5Data[i][TX5_DATA_TIME]
        maxValue = int(tx5Data[i][TX5_DATA_MAX_VALUE])
        minValue = int(tx5Data[i][TX5_DATA_MIN_VALUE])
        lastValue = int(tx5Data[i][TX5_DATA_LAST_VALUE])

        if direction == 0:
            lose = keyPoint - minValue
            win = maxValue - keyPoint

        if direction == 1:
            lose = maxValue - keyPoint
            win = keyPoint - minValue

        if win >= winAmplitude:
            bonus = winAmplitude
            touchTime = time
            break

        if lose >= loseAmplitude:
            bonus = -1 * loseAmplitude
            touchTime = time
            break

        if time >= terminalTime:
            touchTime = time
            if direction == 0:
                bonus = lastValue - keyPoint
            if direction == 1:
                bonus = keyPoint - lastValue
            break

    result["bonus"] = bonus
    result["touchTime"] = touchTime
    return result


def getMaxBonus(tx5Data, breakIndex, direction, keyPoint, terminalTime):
    result = {}
    maxBonus = 0
    touchTime = '00:00:00'
    for i in range(breakIndex+1, len(tx5Data)):
        time = tx5Data[i][TX5_DATA_TIME]
        maxValue = int(tx5Data[i][TX5_DATA_MAX_VALUE])
        minValue = int(tx5Data[i][TX5_DATA_MIN_VALUE])

        if time > terminalTime:
            break

        if (direction == 0) & (maxValue >= keyPoint):
            diff = maxValue - keyPoint
            if diff > maxBonus:
                maxBonus = diff
                touchTime = time

        if (direction == 1) & (minValue <= keyPoint):
            diff = keyPoint - minValue
            if diff > maxBonus:
                maxBonus = diff
                touchTime = time

    result['maxBonus'] = maxBonus
    result['time'] = touchTime

    return result


def getMaxLoss(tx5Data, breakIndex, direction, keyPoint, terminalTime):
    result = {}
    maxLoss = 0
    touchTime = '00:00:00'
    for i in range(breakIndex+1, len(tx5Data)):
        time = tx5Data[i][TX5_DATA_TIME]
        maxValue = int(tx5Data[i][TX5_DATA_MAX_VALUE])
        minValue = int(tx5Data[i][TX5_DATA_MIN_VALUE])

        if time > terminalTime:
            break

        if (direction == 0) & (minValue <= keyPoint):
            diff = minValue - keyPoint
            if diff < maxLoss:
                maxLoss = diff
                touchTime = time

        if (direction == 1) & (maxValue >= keyPoint):
            diff = keyPoint - maxValue
            if diff < maxLoss:
                maxLoss = diff
                touchTime = time

    result['maxLoss'] = maxLoss
    result['time'] = touchTime

    return result
