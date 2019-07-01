from os import listdir

TX5_DATA_DATE = 0
TX5_DATA_TIME = 1
TX5_DATA_OPEN_VALUE = 2
TX5_DATA_MAX_VALUE = 3
TX5_DATA_MIN_VALUE = 4
TX5_DATA_LAST_VALUE = 5
TX5_DATA_VOLUMN = 6


def listTx5Dir(tx5Dir):
    dirList = [tx5Dir + "/" + i for i in listdir(tx5Dir)]
    return dirList


def getTx5Data(file):
    data = open(
        file).readlines()
    data[0:1] = ()
    data1 = [i.strip('\n').strip('\r').split(',') for i in data]
    return data1


def getBaseMaxValue(tx5Data, baseRange, preBreakIndex, perBreakAmplitude):
    maxValue = 0
    for i in range(baseRange):
        maxV = int(tx5Data[i][TX5_DATA_MAX_VALUE])
        lastV = int(tx5Data[i][TX5_DATA_LAST_VALUE])
        if maxV > maxValue:
            if (i >= preBreakIndex) & ((lastV - maxValue) >= perBreakAmplitude):
                break
            else:
                maxValue = maxV
    return maxValue


def getBaseMinValue(tx5Data, baseRange, preBreakIndex, perBreakAmplitude):
    minValue = 1000000
    for i in range(baseRange):
        minV = int(tx5Data[i][TX5_DATA_MIN_VALUE])
        lastV = int(tx5Data[i][TX5_DATA_LAST_VALUE])
        if minV < minValue:
            if (i >= preBreakIndex) & ((minValue - lastV) >= perBreakAmplitude):
                break
            else:
                minValue = minV
    return minValue


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
