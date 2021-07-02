import csv
import sys
from .alphavantage import alphavantage as av

class technicalIndicators(av):
	def __init__(self,api_key):
		av.__init__(self,api_key=api_key)
	def movingAverage(self,scrip = '',typ = 'ema',timeframe='15min',duration='50',series_type='close',datatype='csv'):
		typ = typ.upper()
		scrip = scrip.upper()
		assert(len(scrip) > 0), "Scrip Symbol cannot be empty"
		cExt = 'EMA&symbol='+scrip+'&interval='+timeframe
		cExt += '&time_period='+duration+'&series_type='+series_type
		cExt += '&datatype='+datatype
		data = self.getData(cExt)
		data = list(data)
		if(len(data) < 2):
		 	print("Error receiving Moving Average Data")
		 	return list()
		else:
		 	return data