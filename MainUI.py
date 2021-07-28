#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import *
from levelsfinder import find_levels
import csv
import os.path
from PIL import ImageTk,Image
import mysql.connector
import threading

class MainUI(Tk):
	def __init__(self,keyFile,mydb):
		Tk.__init__(self)
		self.title("Trading Assistant")
		self.geometry("500x500")
		self.scrip_symbol_var = StringVar()
		self.api_key_var = StringVar()
		self.showPlot_var = IntVar()
		self.introFrame = Frame(self)
		self.outputFrame = Frame(self)
		self.keyFile = keyFile
		self.mydb = mydb
		self.scrips = dict()
		self.stockList = None
		self.introFrame.grid(row=0,column=0)
		Button(self.introFrame, text = "Edit Api Keys",\
				command=self.apiKeysUI).grid(row=0,column=0,padx=5,pady=5)
		Button(self.introFrame, text = "Edit Stock List",\
				command=self.stockListUI).grid(row=0,column=1,padx=5,pady=5)
		threading.Thread(target=self.process).start()
		# self.outputFrame.grid(row=3,column=0,rowspan=10)
		# Label(self.inputFrame,text='Scrip Symbol').grid(row=1,column=0,padx=5,pady=5)
		# Entry(self.inputFrame,textvariable=self.scrip_symbol_var).grid(row=1,column=1)
		# Checkbutton(self.inputFrame,text='Show Chart',variable=self.showPlot_var).grid(row=2,column=1)
		# Button(self.inputFrame,text='Submit',command=self.submit).grid(row=2,column=2)

	def process(self):
		self.stockList = self.mydb.stockList()
		for x in self.stockList:
			print(self.mydb.getLatestData(x))


	def apiKeysUI(self):
		apiKeysUIobj = apiKeysUI(self.keyFile)
		apiKeysUIobj.mainloop()

	def stockListUI(self):
		stockListUIobj = stockListUI(self.mydb)
		stockListUIobj.mainloop()

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
		self.keyFile = keyFile
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
		if(not os.path.exists(self.keyFile)):
			Label(self.introFrame,text="0 API keys found. Please\
					 Enter alphavantage API Keys to proceed.")\
						.grid(row=0,column=0)
		else:
			Label(self.introFrame,text="Stored API Keys are:")\
					.grid(row=0,column=0)
			with open(self.keyFile,mode='r') as file:
				csvFile = csv.reader(file)
				for line in csvFile:
					Label(self.mainFrame,text=str(line[0]))\
							.grid(row=self.idx,column=0)
					# Button(self.mainFrame,image=pencilPhoto,command=lambda: self.edit(i)).grid(row=i,column=1)
					# Button(self.mainFrame,image=binPhoto,command=lambda: self.delete(i)).grid(row=i,column=2)
					self.idx += 1
		self.add_button = Button(self.mainFrame,text="Add",\
									command=self.addBox)
		self.submit_button = Button(self.mainFrame,text="Submit",\
									command=self.submit)
		self.addBox()

	def addBox(self):
		if(len(self.api_key_var)):
			if(self.api_key_var[-1].get() == ''):
				return
			if(self.api_key_var[-1].get().find(' ') != -1):
				return
		self.api_key_var.append(Entry(self.mainFrame))
		self.api_key_var[-1].grid(row=self.idx,column=0,padx=2,pady=2)
		self.add_button.grid(row=self.idx,column=1)
		self.submit_button.grid(row=self.idx+1,column=0)
		self.idx += 1

	def submit(self):
		with open(self.keyFile,mode='a') as file:
			Writer = csv.writer(file)
			for api in self.api_key_var:
				api_key = str(api.get())
				if(api_key == ''):
					continue
				Writer.writerow([api_key])
			self.destroy()

class stockListUI(Tk):
	def __init__(self,mydb):
		Tk.__init__(self)
		self.title("Stock List Manager")
		self.geometry("500x500")
		self.mydb = mydb
		self.introFrame = Frame(self)
		self.inputFrame = Frame(self)
		self.introFrame.grid(row=0,column=0,pady=10)
		Label(self.introFrame,text="Enter Stock Symbols")\
				.grid(row=1,column=0)
		self.inputFrame.grid(row=1,column=0)
		self.stock_symbol_var = []
		self.idx = 0
		self.add_button = Button(self.inputFrame,text="Add",\
							command=self.addBox,width=3)
		self.submit_button = Button(self.inputFrame,text="Submit",\
							command=self.submit,width=6)		
		self.addBox()

	def addBox(self):
		if(len(self.stock_symbol_var)):
			if(self.stock_symbol_var[-1].get() == ''):
				return
			elif(self.stock_symbol_var[-1].get().find(' ') != -1):
				return
		self.stock_symbol_var.append(Entry(self.inputFrame))
		self.stock_symbol_var[-1].grid(row=self.idx,column=0,pady=2,padx=2)
		self.add_button.grid(row=self.idx,column=1,padx=2)
		self.submit_button.grid(row=self.idx+1,column=0,padx=2)
		self.idx += 1

	def submit(self):
		for x in self.stock_symbol_var:
			symbol = str(x.get())
			symbol = symbol.upper()
			self.mydb.insertStock(symbol)


