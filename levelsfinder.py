#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from alphavantage.timeseries import timeseries
import csv
import requests
from pprint import pprint
import math
import sys

class _config():
	def __init__(self, api_key):
		self.api_key = api_key
		
def find_levels(data):
	data = list(data)
	idx = {}
	for i in range(len(data[0])):
		idx[data[0][i]] = i
	tolerance = 0.00125
	levels = []
	phigh = 0
	plow = 0
	ahigh = float(data[1][idx['high']])
	alow = float(data[1][idx['low']])
	pp = []
	for row in data[2:]:
		high = float(row[idx['high']])
		ahigh = max(high,ahigh)
		pp.append(high)
		low = float(row[idx['low']])
		alow = min(alow,low)
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
				levels[i][1] += 3
		else:
			del levels[i:i+1]
			i -= 1
		i += 1
	pp.reverse()
	i = 0
	tolerance = 0.007
	while(len(levels) > 10 and i < len(levels)-1):
		if(abs(levels[i][0]-levels[i+1][0]) < tolerance*levels[i][0]):
			if(levels[i][1] > levels[i+1][1]):
				levels.pop(i+1)
			else:
				levels.pop(i)
		else:
			i += 1

	levels.sort(key = lambda x: x[1])
	levels.reverse()
	plt.plot([i for i in range(len(data)-2)],pp)
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
	ts = timeseries(api_key=api_key)
	find_levels(ts.intraday(scrip = scrip))

if __name__ == '__main__':
	main()

