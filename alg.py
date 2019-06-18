import function

TX5_DIR = "/Users/edward_cc_wu/SourceCode/Future/tx5_test"
BASE_RANGE = 3
PRE_BREAK_INDEX = 2
PRE_BREAK_AMPLITUDE = 12
BREAK_AMPLITUDE = 12
BREAK_RANGE = 14  # 10:00:00
RETURN_SCALE = 3
TERMINAL_TIME = "11:30:00"
WIN_AMPLITUDE = 25
LOSE_AMPLITUDE = 26


def go():
    dirs = function.listTx5Dir(TX5_DIR)
    for d in range(len(dirs)):
        if('txt' in dirs[d]):
            trace(dirs[d])


def trace(path):
    tx5Data = function.getTx5Data(path)

    baseMaxValue = function.getBaseMaxValue(
        tx5Data, BASE_RANGE, PRE_BREAK_INDEX, PRE_BREAK_AMPLITUDE)

    baseMinValue = function.getBaseMinValue(
        tx5Data, BASE_RANGE, PRE_BREAK_INDEX, PRE_BREAK_AMPLITUDE)

    print(path)
    out = {}
    out["baseMaxValue"] = baseMaxValue
    out["baseMinValue"] = baseMinValue

    breakIndex = function.getBreakIndex(
        tx5Data, PRE_BREAK_INDEX, baseMaxValue, baseMinValue, BREAK_RANGE)

    direction = function.getBreakDirection(
        tx5Data, PRE_BREAK_INDEX, baseMaxValue, baseMinValue, BREAK_RANGE)

    if breakIndex >= 0 & direction >= 0:
        out["direction"] = ("up", "down")[direction == 1]
        out["breakMaxValue"] = tx5Data[breakIndex][function.TX5_DATA_MAX_VALUE]
        out["breakMinValue"] = tx5Data[breakIndex][function.TX5_DATA_MIN_VALUE]
        out["breakTime"] = tx5Data[breakIndex][function.TX5_DATA_TIME]

        keyPoint = function.getKeyPoint(
            tx5Data, breakIndex, direction, RETURN_SCALE)
        out["keyPoint"] = keyPoint
        maxBonus = function.getMaxBonus(
            tx5Data, breakIndex, direction, keyPoint, TERMINAL_TIME)
        out["maxBonus"] = maxBonus['maxBonus']
        out["maxBonusTime"] = maxBonus['time']
        result = function.getResult(
            tx5Data, breakIndex, direction, keyPoint, TERMINAL_TIME, WIN_AMPLITUDE, LOSE_AMPLITUDE)
        out["result"] = result["bonus"]
        out["resultTime"] = result["touchTime"]

    print(out)
