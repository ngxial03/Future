from common import output, raw_data_gen, raw_data_download
from helper import k
from policy import happy, pre_enter_point, max_min, mm

output.remove()


# os.remove('out/daily.txt')
# os.remove('out/out.txt')
# os.remove('out/out2.txt')

# def listTx5Dir(tx5Dir):
#     dirList = [tx5Dir + "/" + i for i in listdir(tx5Dir)]
#     return dirList

raw_data_download.download()
raw_data_gen.go()
mm.go()
# happy.go()

# k.draw('20210503')

# pre_enter_point.go()

# print(function.getTx5Data('tx5_data/201908/20190816.txt'))

# daily_gen.go()
# alg.go()
# alg2.go()
