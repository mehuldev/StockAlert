import csv
import sys
from .alphavantage import alphavantage as av

class timeseries(av):
	def __init__(self,api_key):
		av.__init__(self,api_key)

	def intraday(self,scrip,timeframe='15min',duration='year1month1',toprint=False):
		cExt = 'TIME_SERIES_INTRADAY_EXTENDED&symbol='
		cExt = cExt+scrip+'&interval='+timeframe
		cExt = cExt+'&slice='+duration+'&datatype=csv'
		data = self.getData(cExt)
		data = list(data)
		assert(len(data) > 1), "***Error in receiving data***"
		if(toprint):
			self._print(data)
		return data

	def _print(self,cr):
			for row in data:
				print(row)



