#!/usr/bin/env python
from MainUI import *
import csv
import os.path
import mysql.connector
from database import myDB

def main():
	keyFile = 'apiKeys.csv'
	mydb = myDB(keyFile=keyFile)
	if(not os.path.exists(keyFile)):
		apiKeysUIobj = apiKeysUI(keyFile)
		apiKeysUIobj.mainloop()
	mydb.cursor.execute("SELECT COUNT(Symbol) FROM scrips")
	for x in mydb.cursor:
		if(x[0] == 0):
			stockListUIobj = stockListUI(mydb)
			stockListUIobj.mainloop()

	MainUIobj = MainUI(keyFile,mydb)
	MainUIobj.mainloop()

if __name__ == '__main__':
	main()