import os
import function
from common import config


def go():
    if not os.path.exists(config.TX_DAILY_DIR):
        writeTitle()
        dirs = function.listTx5Dir(config.TX5_DIR)
        dirs = sorted(dirs)
        for d in range(len(dirs)):
            if 'txt' in dirs[d]:
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
    f = open('out/daily.txt', 'a')
    f.write("%s,%d,%d,%d,%d,%d\n" % (
        out['date'], out['open'], out['high'], out['low'], out['close'], out['volume']))
    f.close()


def writeTitle():
    f = open('out/daily.txt', 'a')
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
        volume = volume + int(tx5Data[i][function.TX5_DATA_VOLUMN])
    return volume
