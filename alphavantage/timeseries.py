import csv
import requests
import sys

class timeseries():
	def __init__(self,api_key):
		self.api_key = api_key
		self.url = 'https://www.alphavantage.co/query?apikey='+self.api_key
		self.url = self.url+'&function='

	def intraday(self,scrip,timeframe='15min',duration='year1month1',toprint=False):
		self.symbol = scrip
		self.timeframe = timeframe
		currurl = self.url+'TIME_SERIES_INTRADAY_EXTENDED&symbol='
		currurl = currurl+scrip+'&interval='+timeframe
		currurl = currurl+'&slice='+duration+'&datatype=csv'
		try:
			data = self.get_data(currurl)
		except:
			print("Error in receiving data")
			sys.exit()

		# print(currurl)
		if(toprint):
			self._print(data)
		return data

	def get_data(self,currurl):
		with requests.Session() as s:
			download = s.get(currurl)
			decoded_content = download.content.decode('utf-8')
			cr = csv.reader(decoded_content.splitlines(),delimiter=',')
			return cr

	def _print(self,cr):
			data = list(cr)
			for row in data:
				print(row)



