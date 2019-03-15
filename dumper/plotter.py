import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import pickle as rick
from model.entry import Entry
data = rick.load(open("./data/2000799148_husets", "rb"))
datelist = []
valuelist = []
for entry in data:
	datelist.append(entry.date)
	valuelist.append(entry.values['husets_elforbrug'])

l = plt.plot(datelist, valuelist)
plt.setp(l, markersize=5)
plt.setp(l, markerfacecolor='C0')
plt.xticks(rotation='vertical');
plt.show()