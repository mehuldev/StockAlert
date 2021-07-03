import requests
import sys
import csv

class alphavantage(object):
	def __init__(self,api_key1='',api_key2 = 'fdfkjfd',output_format='csv'):
		assert(len(api_key1) > 0), "api_key cannot be empty"
		self.api_key1 = api_key1
		self.api_key2 = api_key2
		self.av_url = "https://www.alphavantage.co/query?function="
		self.cnt = 0

	def getData(self,extension):
		# print(self.av_url+extension)
		reqUrl = ''
		if(self.cnt < 5):
			reqUrl = self.av_url+extension+"&apikey="+self.api_key1
			self.cnt += 1
		elif(self.cnt < 10):
			reqUrl = self.av_url+extension+"&apikey="+self.api_key2
			self.cnt += 1
		else:
			reqUrl = self.av_url+extension+"&apikey="+self.api_key1
			self.cnt = 1
		with requests.Session() as s:
			try:
				download = s.get(reqUrl)
				decoded_data = download.content.decode('utf-8')
				cr = csv.reader(decoded_data.splitlines(), delimiter=',')
				return cr
			except:
				print("***Error Sending Request***")
				sys.exit()


