#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from alphavantage.timeseries import timeseries
import csv
import requests
from pprint import pprint
import math

class _config():
	def __init__(self, api_key):
		self.api_key = api_key
		

def find_support(data):
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
	# i = 0
	# ii = []
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
			levels[i] = s/(j-i)
			
		i += 1
	pp.reverse()
	plt.plot([i for i in range(len(data)-2)],pp)
	for j in levels:
		plt.axhline(j, color = 'r',linestyle=':')
	plt.show()

def main():
	# print("Enter API key:",end = ' ')
	# api_key = input()
	api_key = 'FZY90EMEKTOEJTOD'
	config = _config(api_key)
	print("Enter scrip symbol:",end = ' ')
	scrip = input()
	scrip = scrip.upper()
	ts = timeseries(api_key=api_key)
	find_support(ts.intraday(scrip = scrip))

if __name__ == '__main__':
	main()

