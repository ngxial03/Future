import os
import function

#TX5_DIR = "C:/cygwin64/home/Edward_Wu/SourceCodes/Future/tx5_test"
TX5_DIR = "/Users/edward_cc_wu/SourceCode/Future/tx5_test"
TX_DAILY_DIR = "/Users/edward_cc_wu/SourceCode/Future/daily.txt"


def go():
    if not os.path.exists(TX_DAILY_DIR):
        writeTitle()
        dirs = function.listTx5Dir(TX5_DIR)
        dirs = sorted(dirs)
        for d in range(len(dirs)):
            if('txt' in dirs[d]):
                trace(dirs[d])


def trace(path):
    print(path)
    tx5Data = function.getTx5Data(path)

    out = {}
    out['date'] = tx5Data[0][function.TX5_DATA_DATE]
    out['high'] = getHighValue(tx5Data)
    out['low'] = getLowValue(tx5Data)
    out['open'] = getOpenValue(tx5Data)
    out['close'] = getCloseValue(tx5Data)
    out['volume'] = getVolume(tx5Data)

    writeToFile(out)


def writeToFile(out):
    f = open('daily.txt', 'a')
    f.write("%s,%d,%d,%d,%d,%d\n" % (
        out['date'], out['open'], out['high'], out['low'], out['close'], out['volume']))
    f.close()


def writeTitle():
    f = open('daily.txt', 'a')
    f.write("%s,%s,%s,%s,%s,%s\n" %
            ('date', 'open', 'high', 'low', 'close', 'volume'))
    f.close()


def getHighValue(tx5Data):
    maxValue = 0
    for i in range(len(tx5Data)):
        maxV = int(tx5Data[i][function.TX5_DATA_MAX_VALUE])
        if maxV > maxValue:
            maxValue = maxV
    return maxValue


def getLowValue(tx5Data):
    minValue = 100000
    for i in range(len(tx5Data)):
        minV = int(tx5Data[i][function.TX5_DATA_MIN_VALUE])
        if minV < minValue:
            minValue = minV
    return minValue


def getOpenValue(tx5Data):
    openValue = 0
    for i in range(len(tx5Data)):
        openValue = int(tx5Data[i][function.TX5_DATA_OPEN_VALUE])
        break
    return openValue


def getCloseValue(tx5Data):
    lastValue = 0
    for i in range(len(tx5Data)):
        lastValue = int(tx5Data[i][function.TX5_DATA_LAST_VALUE])
    return lastValue


def getVolume(tx5Data):
    volume = 0
    for i in range(len(tx5Data)):
        volume = volume+int(tx5Data[i][function.TX5_DATA_VOLUMN])
    return volume
