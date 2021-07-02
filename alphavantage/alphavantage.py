import requests
import sys
import csv

class alphavantage(object):
	def __init__(self,api_key='',output_format='csv'):
		assert(len(api_key) > 0), "api_key cannot be empty"
		self.api_key = api_key
		self.av_url = "https://www.alphavantage.co/query?apikey="+self.api_key
		self.av_url += "&function="

	def getData(self,extension):
		# print(self.av_url+extension)
		with requests.Session() as s:
			try:
				download = s.get(self.av_url+extension)
				decoded_data = download.content.decode('utf-8')
				cr = csv.reader(decoded_data.splitlines(), delimiter=',')
				return cr
			except:
				print("***Error Sending Request***")
				sys.exit()


