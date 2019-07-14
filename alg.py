import function
import function2

TX5_DIR = "C:/cygwin64/home/Edward_Wu/SourceCodes/Future/tx5_test"
#TX5_DIR = "/Users/edward_cc_wu/SourceCode/Future/tx5_test"
TX_DAILY_DIR = "C:/cygwin64/home/Edward_Wu/SourceCodes/Future/daily.txt"
#TX_DAILY_DIR = "/Users/edward_cc_wu/SourceCode/Future/daily.txt"
BASE_RANGE = 3
PRE_BREAK_INDEX = 2
PRE_BREAK_AMPLITUDE = 5
BREAK_AMPLITUDE = 12
BREAK_RANGE = 14  # 10:00:00
RETURN_SCALE = 3
TERMINAL_TIME = "11:30:00"
WIN_AMPLITUDE = 26
LOSE_AMPLITUDE = 26

g_total = 0


def go():
    writeTitle()
    dirs = function.listTx5Dir(TX5_DIR)
    dirs = sorted(dirs)
    for d in range(len(dirs)):
        if('txt' in dirs[d]):
            trace(dirs[d])
    writeTotal()


def trace(path):
    print(path)
    dailyData = function2.getDailyData(TX_DAILY_DIR)
    tx5Data = function.getTx5Data(path)

    baseMaxValue = function.getBaseMaxValue(
        tx5Data, BASE_RANGE, PRE_BREAK_INDEX, PRE_BREAK_AMPLITUDE)

    baseMinValue = function.getBaseMinValue(
        tx5Data, BASE_RANGE, PRE_BREAK_INDEX, PRE_BREAK_AMPLITUDE)

    out = {}
    diff = function2.getDiff(dailyData, tx5Data[0][function.TX5_DATA_DATE])
    out['diff'] = diff

    out['baseMaxValue'] = baseMaxValue
    out['baseMinValue'] = baseMinValue

    breakIndex = function.getBreakIndex(
        tx5Data, PRE_BREAK_INDEX, baseMaxValue, baseMinValue, BREAK_RANGE)

    direction = function.getBreakDirection(
        tx5Data, PRE_BREAK_INDEX, baseMaxValue, baseMinValue, BREAK_RANGE)

    out['date'] = tx5Data[0][function.TX5_DATA_DATE]
    if breakIndex >= 0 & direction >= 0:
        out['direction'] = ("up", "down")[direction == 1]
        out['breakMaxValue'] = int(
            tx5Data[breakIndex][function.TX5_DATA_MAX_VALUE])
        out['breakMinValue'] = int(
            tx5Data[breakIndex][function.TX5_DATA_MIN_VALUE])
        out['breakTime'] = tx5Data[breakIndex][function.TX5_DATA_TIME]

        keyPoint = function.getKeyPoint(
            tx5Data, breakIndex, direction, RETURN_SCALE)
        out['keyPoint'] = keyPoint

        result = function.getResult(
            tx5Data, breakIndex, direction, keyPoint, TERMINAL_TIME, WIN_AMPLITUDE, LOSE_AMPLITUDE)
        out['result'] = result['bonus']
        out['resultTime'] = result['touchTime']

        maxBonus = function.getMaxBonus(
            tx5Data, breakIndex, direction, keyPoint, TERMINAL_TIME)
        out['maxBonus'] = maxBonus['maxBonus']
        out['maxBonusTime'] = maxBonus['time']

        maxLoss = function.getMaxLoss(
            tx5Data, breakIndex, direction, keyPoint, out['resultTime'])
        out['maxLoss'] = maxLoss['maxLoss']
        out['maxLossTime'] = maxLoss['time']
    else:
        out['direction'] = "-"
        out['breakMaxValue'] = 0
        out['breakMinValue'] = 0
        out['breakTime'] = '00:00:00'
        out['keyPoint'] = 0
        out['maxBonus'] = 0
        out['maxBonusTime'] = '00:00:00'
        out['maxLoss'] = 0
        out['maxLossTime'] = '00:00:00'
        out['result'] = 0
        out['resultTime'] = '00:00:00'

    global g_total
    g_total = g_total + out['result']
    writeToFile(out)


def writeToFile(out):
    f = open('out.txt', 'a')
    # print(out[(out.keys()[10])])
    baseDiff = out['baseMaxValue'] - out['baseMinValue']
    breakDiff = out['breakMaxValue'] - out['breakMinValue']
    f.write("%10s%16d%16d%16d%12d%17d%17d%13s%13d%12d%13s%12d%16s%12d%16s%10d%14s\n" % (out['date'], out['diff'], out['baseMaxValue'],
                                                                                    out['baseMinValue'], baseDiff, out['breakMaxValue'], out[
        'breakMinValue'], out['breakTime'], breakDiff,
        out['keyPoint'], out['direction'], out['maxBonus'], out['maxBonusTime'],
        out['maxLoss'], out['maxLossTime'],
        out['result'], out['resultTime']))

    f.close()


def writeTitle():
    f = open('out.txt', 'a')
    f.write("%10s%16s%16s%16s%12s%17s%17s%13s%13s%12s%13s%12s%16s%12s%16s%10s%14s\n\n" % ('date', 'diff', 'baseMaxValue', 'baseMinValue', 'baseDiff',
                                                                                      'breakMaxValue', 'breakMinValue', 'breakTime', 'breakDiff', 'keyPoint',
                                                                                      'direction', 'maxBonus', 'maxBonusTime', 'maxLoss', 'maxLossTime', 'result', 'resultTime'))
    f.close()


def writeTotal():
    f = open('out.txt', 'a')
    global g_total
    f.write("\n\n%s\t%d\n\n" % ('total:', g_total))
    f.close()
