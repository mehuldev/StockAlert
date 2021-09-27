import mysql.connector
from levelsfinder import *

class myDB():
	def __init__(self,keyFile):
		self.mydb = None
		self.keyFile = keyFile
		self.stockList = []
		self.tables = ['scrips','levels','ema50','ema200']
		self.validate_database()

	def create_database(self):
		self.mydb = mysql.connector.connect(
			host='localhost',
			user='mehul',
			password='1234')
		cursor = self.mydb.cursor()
		cursor.execute("CREATE DATABASE mydb")
		cursor.close()

	def create_tables(self):
		cursor = self.mydb.cursor()
		cursor.execute("SHOW TABLES")
		tables = [x[0] for x in cursor]
		if('scrips' not in tables):
			cursor.execute("CREATE TABLE `scrips` \
				(`Symbol` VARCHAR(255) NOT NULL,\
					`Price` DECIMAL(19,2),\
					PRIMARY KEY (`Symbol`)\
				)")
		if('levels' not in tables):
			cursor.execute("CREATE TABLE `levels` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				`Level` DECIMAL(19,2),\
				`Strength` DECIMAL(19,1)\
				)")
		if('ema50' not in tables):
			cursor.execute("CREATE TABLE `ema50` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				`15min` DECIMAL(19,2),\
				 `60min` DECIMAL(19,2),\
				  `daily` DECIMAL(19,2) \
				)")
		if('ema200' not in tables):
			cursor.execute("CREATE TABLE `ema200` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				`15min` DECIMAL(19,2),\
				 `60min` DECIMAL(19,2),\
				  `daily` DECIMAL(19,2) \
				)")
		cursor.close()

	def validate_database(self):
		try:
			self.mydb = mysql.connector.connect(
				host='localhost',
				user='mehul',
				password='1234',
				database='mydb')
		except:
			self.create_database()
		self.create_tables()

	def insertStock(self,symbol: str):
		cursor = self.mydb.cursor()
		command = ("SELECT Symbol FROM scrips WHERE Symbol='{}'".format(symbol))
		cursor.execute(command)
		l = 0
		for x in cursor:
			if(x[0].upper() == symbol):
				l += 1
		if(l == 0):
			command = ("INSERT INTO scrips (Symbol, Price) VALUES(%s,%s)")
			entry = (symbol,'0.0')
			cursor.execute(command,entry)

		else:
			command = ("UPDATE scrips SET Symbol='{}' WHERE Symbol LIKE UPPER('%{}')".format(symbol,symbol))
			cursor.execute(command)
		self.mydb.commit()
		cursor.close()

	def get_stock_list(self) -> list: 
		cursor = self.mydb.cursor()
		cursor.execute("SELECT Symbol FROM scrips")
		data = [x[0] for x in cursor]
		cursor.close()
		return data

	def updateLevels(self, scrip: str):
		cursor = self.mydb.cursor()
		data = find_levels(scrip=scrip,keyFile=self.keyFile)
		for table in self.tables[1:]:
			command = "DELETE FROM {} WHERE Symbol='{}'".format(table,symbol)
			cursor.execute(command)
			if(table == 'levels'):
				command = "INSERT INTO levels(Symbol, Level, Strength) VALUES (%s,%s,%s)"
				val = [(scrip,x,y) for x,y in data[table]]
			else:
				command = "INSERT INTO {}(Symbol,15min,60min,daily) VALUES (%s,%s,%s,%s)".format(table)
				val = [(scrip,data[table][0],data[table][1],data[table][2])]
			cursor.executemany(command,val)
		self.mydb.commit()
		cursor.close()

	def get_latest_data_all(self):
		if(len(self.stockList) == 0):
			self.stockList = self.get_stock_list()
		cursor = self.mydb.cursor(buffered=True)
		data = current_price(stockList=self.stockList,keyFile=self.keyFile)
		command = "UPDATE scrips SET Price= %s WHERE Symbol=%s"
		records_to_update = list(zip(data.values(),data.keys()))
		cursor.executemany(command,records_to_update)
		self.mydb.commit()
		cursor.close()
		return data
