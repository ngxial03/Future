from common import output
from common import daily_gen
from policy import alg, alg2
from os import listdir
import os

output.remove()

#os.remove('out/daily.txt')
# os.remove('out/out.txt')
# os.remove('out/out2.txt')

def listTx5Dir(tx5Dir):
    dirList = [tx5Dir + "/" + i for i in listdir(tx5Dir)]
    return dirList

print(listTx5Dir('tx5_data/'))

# daily_gen.go()
# alg.go()
# alg2.go()


