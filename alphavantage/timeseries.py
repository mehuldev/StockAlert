import csv
import sys
from .alphavantage import alphavantage as av
import threading
import concurrent.futures
class timeseries(av):
	def __init__(self,keyFile):
		# self.API_keys = []
		# with open(keyFile,mode='r') as file:
		# 	csvFile = csv.reader(file)
		# 	for line in csvFile:
		# 		self.API_keys.append(line[0])
		# 	file.close()
		av.__init__(self,keyFile=keyFile)

	def intraday_single(self,scrip,timeframe='15min',duration='year1month1'):
		if(timeframe == '1min'):
			cExt = 'TIME_SERIES_INTRADAY'
		else:
			cExt = 'TIME_SERIES_INTRADAY_EXTENDED'
		cExt = cExt+'&symbol='
		cExt = cExt+scrip+'&interval='+timeframe
		cExt = cExt+'&slice='+duration+'&datatype=csv'
		cExt += "&adjusted=false"
		data = self.getData(cExt)
		data = list(data)
		# print(data)
		assert(len(data) > 1), "***Error in receiving data***"
		return data



