#!/usr/bin/env python
from MainUI import *
import csv
import os.path
import mysql.connector
from database import myDB

def main():
	keyFile = 'apiKeys.csv'
	mydb = myDB()
	if(not os.path.exists(keyFile)):
		apiKeysUIobj = apiKeysUI(keyFile)
		apiKeysUIobj.mainloop()
	mydb.mycursor.execute("SELECT COUNT(Symbol) FROM scrips")
	for x in mydb.mycursor:
		if(x[0] == 0):
			stockListUIobj = stockListUI(mydb)
			stockListUIobj.mainloop()

	MainUIobj = MainUI()
	MainUIobj.mainloop()

if __name__ == '__main__':
	main()