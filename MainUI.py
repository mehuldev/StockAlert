#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import *
from levelsfinder import find_levels
import csv
import os.path
from PIL import ImageTk,Image
import mysql.connector

class MainUI(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title("Trading Assistant")
		self.geometry("500x500")
		self.scrip_symbol_var = StringVar()
		self.api_key_var = StringVar()
		self.showPlot_var = IntVar()
		self.inputFrame = Frame(self)
		self.outputFrame = Frame(self)
		self.inputFrame.grid(row=0,column=0,rowspan=3)
		self.outputFrame.grid(row=3,column=0,rowspan=10)
		Label(self.inputFrame,text='Scrip Symbol').grid(row=1,column=0,padx=5,pady=5)
		Entry(self.inputFrame,textvariable=self.scrip_symbol_var).grid(row=1,column=1)
		Checkbutton(self.inputFrame,text='Show Chart',variable=self.showPlot_var).grid(row=2,column=1)
		Button(self.inputFrame,text='Submit',command=self.submit).grid(row=2,column=2)
	def submit(self):
		api_key = self.api_key_var.get()
		scrip = self.scrip_symbol_var.get()
		showPlot = self.showPlot_var.get()
		levels = find_levels(api_key=api_key,scrip=scrip,showPlot=showPlot)
		Label(self.outputFrame,text='Levels').grid(row=0,column=1,padx=10)
		Label(self.outputFrame,text='Strength').grid(row=0,column=2,padx=10)
		for i in range(len(levels)):
			Label(self.outputFrame,text=str(levels[i][0])).grid(row=i+1,column=1,padx=10)
			Label(self.outputFrame,text=str(levels[i][1])).grid(row=i+1,column=2,padx=10)

class apiKeysUI(Tk):
	def __init__(self,keyFile):
		Tk.__init__(self)
		self.title("API Key Manager")
		self.geometry("500x500")
		self.apiFile = keyFile
		self.introFrame = Frame(self)
		self.mainFrame = Frame(self)
		self.introFrame.grid(row=0,column=0,pady=10)
		self.mainFrame.grid(row=1,column=0)
		self.idx = 0
		# Button(self.mainFrame,text="Exit",command=self.destroy).grid(row=0,column=0)
		self.api_key_var = []
		# pencilPhoto = ImageTk.PhotoImage(Image.open('pencil.jpeg'))
		# binPhoto = ImageTk.PhotoImage(Image.open('bin.jpeg'))
		# savePhoto = ImageTk.PhotoImage(Image.open("save.png").resize((1,1)))
		if(not os.path.exists(self.apiFile)):
			Label(self.introFrame,text="0 API keys found. Please Enter alphavantage API Keys to proceed.").grid(row=0,column=0)
		else:
			Label(self.introFrame,text="Stored API Keys are:").grid(row=0,column=0)
			with open(self.apiFile,mode='r') as file:
				csvFile = csv.reader(file)
				for line in csvFile:
					Label(self.mainFrame,text=str(line[0])).grid(row=self.idx,column=0)
					# Button(self.mainFrame,image=pencilPhoto,command=lambda: self.edit(i)).grid(row=i,column=1)
					# Button(self.mainFrame,image=binPhoto,command=lambda: self.delete(i)).grid(row=i,column=2)
					self.idx += 1
		self.add_button = Button(self.mainFrame,text="Add",command=self.addBox)
		self.submit_button = Button(self.mainFrame,text="Submit",command=self.submit)
		self.addBox()

	def addBox(self):
		if(len(self.api_key_var)):
			if(self.api_key_var[-1].get() == ''):
				return
			if(self.api_key_var[-1].get().find(' ') != -1):
				return
		temp = Entry(self.mainFrame)
		temp.grid(row=self.idx,column=0,padx=2,pady=2)
		self.api_key_var.append(temp)
		self.add_button.grid(row=self.idx,column=1)
		self.submit_button.grid(row=self.idx+1,column=0)
		self.idx += 1

	def submit(self):
		with open(self.apiFile,mode='a') as file:
			Writer = csv.writer(file)
			for api in self.api_key_var:
				api_key = str(api.get())
				if(api_key == ''):
					continue
				Writer.writerow([api_key])
			self.destroy()

class stockListUI(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.title("Stock Symbol Manager")
		self.geometry("500x500")
		self.introFrame = Frame(self)
		self.inputFrame = Frame(self)
		# self.introFrame.grid(row=0,column=0,pady=10)
		self.inputFrame.grid(row=1,column=0)
		self.stock_symbol_var = []
		self.idx = 0
		self.add_button = Button(self.inputFrame,text="Add",command=self.addBox,width=3)
		self.submit_button = Button(self.inputFrame,text="Submit",command=self.submit,width=6)		
		self.addBox()

	def addBox(self):
		if(len(self.stock_symbol_var)):
			if(self.stock_symbol_var[-1].get() == ''):
				return
			elif(self.stock_symbol_var[-1].get().find(' ') != -1):
				return
		temp = Entry(self.inputFrame)
		temp.grid(row=self.idx,column=0,pady=2)
		self.stock_symbol_var.append(temp)
		self.add_button.grid(row=self.idx,column=1)
		self.submit_button.grid(row=self.idx+1,column=0)
		self.idx += 1

	def submit(self):
		mydb = None
		mycursor = None
		try:
			mydb = mysql.connector.connect(
				host='localhost',
				user='mehul',
				password='1234',
				database='mydb')
		except:
			mydb = mysql.connector.connect(
				host='localhost',
				user='mehul',
				password='1234')
			mycursor = mydb.cursor()
			mycursor.execute("CREATE DATABASE mydb")
		mycursor = mydb.cursor()
		mycursor.execute("SHOW TABLES")
		tables = [x[0] for x in mycursor]
		if('scrips' not in tables):
			mycursor.execute("CREATE TABLE `scrips` \
				(`Symbol` VARCHAR(255) NOT NULL,\
					`Price` DECIMAL(5,3),\
					PRIMARY KEY (`Symbol`)\
				)")
		if('levels' not in tables):
			mycursor.execute("CREATE TABLE `levels` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				FOREIGN KEY (`Symbol`) REFERENCES scrips(`Symbol`),\
				`level` DECIMAL(5,3),\
				`Strength` DECIMAL(2,1)\
				)")
		if('ema50' not in tables):
			mycursor.execute("CREATE TABLE `ema50` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				FOREIGN KEY (Symbol) REFERENCES scrips(Symbol),\
				`15min` DECIMAL(5,3),\
				 `60min` DECIMAL(5,3),\
				  `daily` DECIMAL(5,3) \
				)")
		if('ema200' not in tables):
			mycursor.execute("CREATE TABLE `ema200` \
				(`Symbol` VARCHAR(255) NOT NULL,\
				FOREIGN KEY (`Symbol`) REFERENCES scrips(`Symbol`),\
				`15min` DECIMAL(5,3),\
				 `60min` DECIMAL(5,3),\
				  `daily` DECIMAL(5,3) \
				)")
		for x in self.stock_symbol_var:
			symbol = str(x.get())
			symbol = symbol.upper()
			command = ("SELECT Symbol FROM scrips WHERE Symbol='{}'".format(symbol))
			mycursor.execute(command)
			l = 0
			for x in mycursor:
				if(x[0].upper() == symbol):
					l += 1
			if(l == 0):
				command = ("INSERT INTO scrips (Symbol, Price) VALUES(%s,%s)")
				entry = (symbol,'0.0')
				mycursor.execute(command,entry)

			else:
				command = ("UPDATE scrips SET Symbol='{}' WHERE Symbol LIKE UPPER('%{}')".format(symbol,symbol))
				mycursor.execute(command)
			mydb.commit()


