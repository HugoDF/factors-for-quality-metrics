import matplotlib.pyplot as plt
from numpy import corrcoef

import json

def plot(xs, ys):
    plt.plot(xs,ys)
    plt.show()


with open('./data/sizeVsFailureRate.json') as data_file:
    data = json.load(data_file)
    sizes, failureRate = data
    plot(sizes, failureRate)
