from common import output
from common import daily_gen
from policy import alg, alg2
import os

output.remove()

#os.remove('out/daily.txt')
# os.remove('out/out.txt')
# os.remove('out/out2.txt')

daily_gen.go()
alg.go()
alg2.go()


