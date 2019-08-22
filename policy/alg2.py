from common import config, function, function2

#TX5_DIR = "C:/cygwin64/home/Edward_Wu/SourceCodes/Future/tx5_test"
# TX5_DIR = "/Users/edward_cc_wu/SourceCode/Future/tx5_test"
#TX_DAILY_DIR = "C:/cygwin64/home/Edward_Wu/SourceCodes/out/Future/daily.txt"
# TX_DAILY_DIR = "/Users/edward_cc_wu/SourceCode/Future/out/daily.txt"

DIFF_AMPLITUDE = 100
TERMINAL_TIME = "11:30:00"


def go():
    writeTitle()
    dirs = function.listTx5Dir(config.TX5_DIR)
    dirs = sorted(dirs)
    dailyData = function2.getDailyData(config.TX_DAILY_DIR)
    for d in range(len(dirs)):
        if('txt' in dirs[d]):
            trace(dirs[d], dailyData)


def trace(path, dailyData):
    tx5Data = function.getTx5Data(path)
    out = {}
    diff = function2.getDiff(dailyData, tx5Data[0][function.TX5_DATA_DATE])
    keyPoint = function2.getKeyPoint(
        dailyData, tx5Data[0][function.TX5_DATA_DATE])
    direction = 0 if diff > 0 else 1
    maxBonus = function.getMaxBonus(
        tx5Data, 1, direction, keyPoint, TERMINAL_TIME)
    maxLoss = function.getMaxLoss(
        tx5Data, 1, direction, keyPoint, TERMINAL_TIME)
    out['date'] = tx5Data[0][function.TX5_DATA_DATE]
    out['diff'] = diff
    out['maxBonus'] = maxBonus['maxBonus']
    out['maxBonusTime'] = maxBonus['time']
    out['maxLoss'] = maxLoss['maxLoss']
    out['maxLossTime'] = maxLoss['time']
    writeToFile(out)


def writeToFile(out):
    f = open('out/out2.txt', 'a')
    # print(out[(out.keys()[10])])

    print(out)
    f.write("%10s%16d%16d%16s%16d%16s\n" % (out['date'], out['diff'], out['maxBonus'], out['maxBonusTime'], out['maxLoss'], out['maxLossTime']))

    f.close()


def writeTitle():
    f = open('out/out2.txt', 'a')
    f.write("%10s%16s%16s%16s%16s%16s\n\n" % ('date', 'diff', 'maxBonus', 'maxBonusTime', 'maxLoss', 'maxLossTime'))
    f.close()
