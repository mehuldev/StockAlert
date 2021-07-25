import mysql.connector

class myDB():
	def __init__(self):
		self.mydb = None
		self.mycursor = None
		self.validate_database()

	def create_database(self):
		self.mydb = mysql.connector.connect(
			host='localhost',
			user='mehul',
			password='1234')
		self.mycursor = self,mydb.cursor()
		self.mycursor.execute("CREATE DATABASE mydb")

	def create_tables(self):
		self.mycursor = self.mydb.cursor()
		self.mycursor.execute("SHOW TABLES")
		tables = [x[0] for x in self.mycursor]
		if('scrips' not in tables):
			self.mycursor.execute("CREATE TABLE `scrips` \
				(`Symbol` VARCHAR(255) NOT NULL,\
					`Price` DECIMAL(5,3),\
					PRIMARY KEY (`Symbol`)\
				)")
		if('levels' not in tables):
			self.mycursor.execute("CREATE TABLE `levels` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				FOREIGN KEY (`Symbol`) REFERENCES scrips(`Symbol`),\
				`level` DECIMAL(5,3),\
				`Strength` DECIMAL(2,1)\
				)")
		if('ema50' not in tables):
			self.mycursor.execute("CREATE TABLE `ema50` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				FOREIGN KEY (Symbol) REFERENCES scrips(Symbol),\
				`15min` DECIMAL(5,3),\
				 `60min` DECIMAL(5,3),\
				  `daily` DECIMAL(5,3) \
				)")
		if('ema200' not in tables):
			self.mycursor.execute("CREATE TABLE `ema200` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				FOREIGN KEY (`Symbol`) REFERENCES scrips(`Symbol`),\
				`15min` DECIMAL(5,3),\
				 `60min` DECIMAL(5,3),\
				  `daily` DECIMAL(5,3) \
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
		self.mycursor.execute(command)
		l = 0
		for x in self.mycursor:
			if(x[0].upper() == symbol):
				l += 1
		if(l == 0):
			command = ("INSERT INTO scrips (Symbol, Price) VALUES(%s,%s)")
			entry = (symbol,'0.0')
			self.mycursor.execute(command,entry)

		else:
			command = ("UPDATE scrips SET Symbol='{}' WHERE Symbol LIKE UPPER('%{}')".format(symbol,symbol))
			self.mycursor.execute(command)
		self.mydb.commit()
