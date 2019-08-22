import os
from os import listdir


def remove():
    files = ['out/' + i for i in listdir("out/")]
    for f in range(len(files)):
        os.remove(files[f])


