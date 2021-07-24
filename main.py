#!/usr/bin/env python
from MainUI import *
import csv
import os.path
import mysql.connector

def main():
	keyFile = 'apiKeys.csv'
	if(not os.path.exists('apiKeys.csv')):
		apiKeysUIobj = apiKeysUI(keyFile)
		apiKeysUIobj.mainloop()
	mydb = None
	try:
		mydb = mysql.connector.connect(
			host="localhost",
			user="mehul",
			password="1234",
			database="mydb")
	except:
		stockListUIobj = stockListUI()
		stockListUIobj.mainloop()
		mydb = mysql.connector.connect(
			host='localhost',
			user="mehul",
			password='1234',
			database='mydb')
	MainUIobj = MainUI()
	MainUIobj.mainloop()

if __name__ == '__main__':
	# root = Tk()
	main()