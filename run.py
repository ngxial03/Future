from common import output, function, tx1_helper
from common import daily_gen
from policy import alg, alg2
from os import listdir
import os

output.remove()


# os.remove('out/daily.txt')
# os.remove('out/out.txt')
# os.remove('out/out2.txt')

# def listTx5Dir(tx5Dir):
#     dirList = [tx5Dir + "/" + i for i in listdir(tx5Dir)]
#     return dirList


# tx1_dic = tx1_helper.list_tx1_dir('tx1_data')
# for key in tx1_dic:
#     print (tx1_helper.get_tx1_data(tx1_dic[key][0]))

# print(function.getTx5Data('tx5_data/201908/20190816.txt'))

daily_gen.go()
alg.go()
alg2.go()
