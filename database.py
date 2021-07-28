import mysql.connector
from levelsfinder import *

class myDB():
	def __init__(self,keyFile):
		self.mydb = None
		self.cursor = None
		self.keyFile = keyFile
		self.tables = ['scrips','levels','ema50','ema200']
		self.validate_database()

	def create_database(self):
		self.mydb = mysql.connector.connect(
			host='localhost',
			user='mehul',
			password='1234')
		self.cursor = self,mydb.cursor()
		self.cursor.execute("CREATE DATABASE mydb")

	def create_tables(self):
		self.cursor = self.mydb.cursor()
		self.cursor.execute("SHOW TABLES")
		tables = [x[0] for x in self.cursor]
		if('scrips' not in tables):
			self.cursor.execute("CREATE TABLE `scrips` \
				(`Symbol` VARCHAR(255) NOT NULL,\
					`Price` DECIMAL(19,2),\
					PRIMARY KEY (`Symbol`)\
				)")
		if('levels' not in tables):
			self.cursor.execute("CREATE TABLE `levels` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				`Level` DECIMAL(19,2),\
				`Strength` DECIMAL(19,1)\
				)")
		if('ema50' not in tables):
			self.cursor.execute("CREATE TABLE `ema50` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				`15min` DECIMAL(19,2),\
				 `60min` DECIMAL(19,2),\
				  `daily` DECIMAL(19,2) \
				)")
		if('ema200' not in tables):
			self.cursor.execute("CREATE TABLE `ema200` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				`15min` DECIMAL(19,2),\
				 `60min` DECIMAL(19,2),\
				  `daily` DECIMAL(19,2) \
				)")

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
		command = ("SELECT Symbol FROM scrips WHERE Symbol='{}'".format(symbol))
		self.cursor.execute(command)
		l = 0
		for x in self.cursor:
			if(x[0].upper() == symbol):
				l += 1
		if(l == 0):
			command = ("INSERT INTO scrips (Symbol, Price) VALUES(%s,%s)")
			entry = (symbol,'0.0')
			self.cursor.execute(command,entry)

		else:
			command = ("UPDATE scrips SET Symbol='{}' WHERE Symbol LIKE UPPER('%{}')".format(symbol,symbol))
			self.cursor.execute(command)
		self.mydb.commit()

	def stockList(self) -> list: 
		self.cursor.execute("SELECT Symbol FROM scrips")		
		return [x[0] for x in self.cursor]

	def updateLevels(self, symbol: str):
		data = find_levels(scrip=symbol,keyFile=self.keyFile)
		for table in self.tables[1:]:
			command = "DELETE FROM {} WHERE Symbol='{}'".format(table,symbol)
			self.cursor.execute(command)
			if(table == 'levels'):
				command = "INSERT INTO levels(Symbol, Level, Strength) VALUES (%s,%s,%s)"
				val = [(symbol,x,y) for x,y in data[table]]
			else:
				command = "INSERT INTO {}(Symbol,15min,60min,daily) VALUES (%s,%s,%s,%s)".format(table)
				val = [(symbol,data[table][0],data[table][1],data[table][2])]
			self.cursor.executemany(command,val)
		self.mydb.commit()

	def getLatestData(self, symbol: str):
		command = "SELECT COUNT(Symbol) from levels WHERE Symbol='{}'".format(symbol)
		self.cursor.execute(command)
		for x in self.cursor:
			if(x[0] == 0):
				self.updateLevels(scrip=symbol)
		data = current_price(scrip=symbol,keyFile=self.keyFile)
		command = "UPDATE scrips SET Price='{}' WHERE Symbol='{}'".format(data,symbol)
		self.cursor.execute(command)
		self.mydb.commit()
		return data
