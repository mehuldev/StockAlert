import requests
import sys
import csv
# import os

class alphavantage(object):
	def __init__(self,keyFile,output_format='csv'):
		self.keyFile = keyFile
		self.apiKeys = []
		# os.path('../')
		with open(self.keyFile,mode='r') as file:
			csvFile = csv.reader(file)
			for line in csvFile:
				self.apiKeys.append(line[0])
			file.close()
		self.av_url = "https://www.alphavantage.co/query?function="

	def getData(self,extension):
		reqUrl = ''
		reqUrl = self.av_url+extension+"&apikey="+self.apiKeys[0]
		self.apiKeys.append(self.apiKeys.pop(0))
		with requests.Session() as s:
			try:
				download = s.get(reqUrl)
				decoded_data = download.content.decode('utf-8')
				cr = csv.reader(decoded_data.splitlines(), delimiter=',')
				return cr
			except:
				print("***Error Sending Request***")
				sys.exit()