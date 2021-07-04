#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from alphavantage.timeseries import timeseries
from alphavantage.technicalIndicators import technicalIndicators
import csv
import math
import sys
import pandas as pd

class _config():
	def __init__(self, api_key):
		self.api_key = api_key
	
def find_levels(scrip,ts,ti):
	data = ts.intraday(scrip=scrip, duration='year1month1')
	data = data+ts.intraday(scrip=scrip,duration='year1month2')[1:]
	idx = {}
	for i in range(len(data[0])):
		idx[data[0][i]] = i
	tolerance = 0.00125
	levels = []
	#Previous High
	phigh = 0
	#Previous Low
	plow = 0
	#Absolute high
	ahigh = float(data[1][idx['high']])
	#Absolute low
	alow = float(data[1][idx['low']])
	pp = []
	close15 = []
	close60 = []
	i = 1
	for row in data[1:]:
		high = float(row[idx['high']])
		ahigh = max(high,ahigh)
		pp.append(high)
		low = float(row[idx['low']])
		alow = min(alow,low)
		close15.append(float(row[idx['close']]))
		if(i%4 == 1):
			close60.append(float(row[idx['close']]))
		i += 1
		if(phigh == 0):
			phigh = high
			plow = low
			continue
		op = float(row[idx['open']])
		close = float(row[idx['close']])
		# Lower highs
		if(phigh-high >= phigh*tolerance):
			levels.append(phigh)
		# Higher Lows
		elif(low-plow >= plow*tolerance):
			levels.append(plow)
		phigh = high
		plow = low
	close15 = pd.DataFrame({'A':close15[::-1]})
	close60 = pd.DataFrame({'B':close60[::-1]})
	ema50 = [close15.ewm(span=50).mean(),close60.ewm(span=50).mean()]
	ema200 = [close15.ewm(span=200).mean(),close60.ewm(span=200).mean()]
	ema50 = [list(ema50[0]['A'])[-1],list(ema50[1]['B'])[-1]]
	ema200 = [list(ema200[0]['A'])[-1],list(ema200[1]['B'])[-1]]
	ema50.append(float(ti.movingAverage(timeframe='daily',scrip=scrip,length='50')[1][1]))
	ema200.append(float(ti.movingAverage(scrip=scrip,length='200',timeframe='daily')[1][1]))
	levels.append(alow)
	levels.append(ahigh)
	levels.sort()
	tolerance = 0.005
	i = 0
	while(i < len(levels)):
		j = i+1
		s = levels[i]
		while(j < len(levels) and levels[j]-levels[i] <= tolerance*levels[i]):
			s += levels[j]
			j += 1
		if(s > levels[i]):
			del levels[i:j-1]
			levels[i] = [s/(j-i),(j-i)/5]
			if(levels[i][0]-alow <= tolerance*alow or ahigh-levels[i][0] <= tolerance*ahigh):
				levels[i][1] += 1
			for z in range(len(ema50)):
				if(abs(levels[i][0]-ema50[z]) <= tolerance*ema50[z]):
					levels[i][1] += 0.5*z+1
				elif(abs(levels[i][0]-ema200[z]) <= tolerance*ema200[z]):
					levels[i][1] += z+1
			levels[i][1] = min(levels[i][1],10)
		else:
			del levels[i:i+1]
			i -= 1
		i += 1
	pp.reverse()
	i = 0
	tolerance = 0.005
	while(i > 10 and i < len(levels)-1):
		if(abs(levels[i][0]-levels[i+1][0]) <= tolerance*levels[i][0]):
			if(levels[i][1] > levels[i+1][1]):
				levels.pop(i+1)
			else:
				levels.pop(i)
		else:
			i += 1

	levels.sort(key = lambda x: x[1])
	levels.reverse()
	plt.plot([i for i in range(len(data)-1)],pp)
	for j in levels[:min(len(levels),10)]:
		plt.text(len(data),j[0],j[1])
		plt.axhline(j[0],color = 'r',linestyle=':')
	plt.show()

def main():
	print("Enter Alphavantage API key:",end = ' ')
	api_key = input()
	config = _config(api_key)
	print("Enter scrip symbol:",end = ' ')
	scrip = input()
	scrip = scrip.upper()
	ti = technicalIndicators(api_key1 = api_key)
	ts = timeseries(api_key1 = api_key)
	find_levels(scrip,ts,ti)

if __name__ == '__main__':
	main()

