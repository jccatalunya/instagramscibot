# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 12:35:46 2016

@author: isman7
"""

import csv
import datetime
from pylab import *


timestamp = []
followers = []

with open('followers.log', 'r') as f_log:
    logreader = csv.reader(f_log, delimiter=';')
    for row in logreader:
        timestamp.append(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f'))
        followers.append(int(row[1]))

timestamp_ticks = [date.strftime('%H:%M') if not index%6 else '' for index, date in enumerate(timestamp)]
timestamp_decim = [date.hour + date.minute/60 for date in timestamp]

figure()
plt.xticks(timestamp_decim, timestamp_ticks)
locs, labels = plt.xticks()
plt.setp(labels, rotation=0)
plt.plot(timestamp_decim, followers, 'r.-', label='@joventutcomunistacat followers')
ax = list(plt.axis())
axis([floor(ax[0]), ceil(ax[1]), round(ax[2], -1)-10, round(ax[3], -2)]), 
xlabel('Hour'), ylabel('Followers')
grid()
legend()