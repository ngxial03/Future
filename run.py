from common import output, raw_data_gen
from policy import happy, pre_enter_point

output.remove()


# os.remove('out/daily.txt')
# os.remove('out/out.txt')
# os.remove('out/out2.txt')

# def listTx5Dir(tx5Dir):
#     dirList = [tx5Dir + "/" + i for i in listdir(tx5Dir)]
#     return dirList

raw_data_gen.go()
happy.go()
# pre_enter_point.go()

# print(function.getTx5Data('tx5_data/201908/20190816.txt'))

# daily_gen.go()
# alg.go()
# alg2.go()
