from common import function

DAILY_DATA_DATE = 0
DAILY_DATA_OPEN_VALUE = 1
DAILY_DATA_MAX_VALUE = 2
DAILY_DATA_MIN_VALUE = 3
DAILY_DATA_LAST_VALUE = 4
DAILY_DATA_VOLUMN = 5


def getDailyData(file):
    data = open(
        file).readlines()
    data[0:1] = ()
    data1 = [i.strip('\n').strip('\r').split(',') for i in data]
    return data1


def getKeyPoint(dailyData, date):
    for i in range(len(dailyData)):
        if (dailyData[i][DAILY_DATA_DATE] == date) & (i > 0):
            return int(dailyData[i][DAILY_DATA_OPEN_VALUE])
    return 0


def getDiff(dailyData, date):
    diff = 0
    for i in range(len(dailyData)):
        if (dailyData[i][DAILY_DATA_DATE] == date) & (i > 0):
            diff = int(dailyData[i][DAILY_DATA_OPEN_VALUE]) - int(dailyData[i-1][DAILY_DATA_LAST_VALUE])
            break
    return diff


def getMaxBonus(tx5Data, breakIndex, direction, keyPoint, terminalTime):
    result = {}
    maxBonus = 0
    touchTime = '00:00:00'
    for i in range(breakIndex+1, len(tx5Data)):
        time = tx5Data[i][function.TX5_DATA_TIME]
        maxValue = int(tx5Data[i][function.TX5_DATA_MAX_VALUE])
        minValue = int(tx5Data[i][function.TX5_DATA_MIN_VALUE])

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
        time = tx5Data[i][function.TX5_DATA_TIME]
        maxValue = int(tx5Data[i][function.TX5_DATA_MAX_VALUE])
        minValue = int(tx5Data[i][function.TX5_DATA_MIN_VALUE])

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
