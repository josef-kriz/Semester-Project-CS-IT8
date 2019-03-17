import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pickle as rick
from model.entry import Entry
import sys
import os
data = rick.load(open(sys.argv[1], "rb"))
plotpath = sys.argv[1] + "_plots";
if not os.path.isdir(plotpath):
    os.mkdir(plotpath);
datelist = []
for entry in data:
	datelist.append(entry.date)

for key in entry.values:
    valuelist = []
    for entry in data:
        valuelist.append(entry.values[key])
    plot = plt.plot(datelist, valuelist)
    plt.setp(plot, markersize=5)
    plt.setp(plot, markerfacecolor='C0')
    plt.suptitle(key)
    plt.xticks(rotation='vertical')
    plt.savefig(sys.argv[1] + "_plots/" + key +".png")
    plt.clf()


