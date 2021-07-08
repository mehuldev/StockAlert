#!/usr/bin/env python
from tkinter import *
from tkinter.ttk import *
from levelsfinder import *

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
		Label(self.inputFrame,text='Api Key').grid(row=0,column=0,padx=5,pady=5)
		Entry(self.inputFrame,textvariable=self.api_key_var).grid(row=0,column=1)
		Label(self.inputFrame,text='Scrip Symbol').grid(row=1,column=0,padx=5,pady=5)
		Entry(self.inputFrame,textvariable=self.scrip_symbol_var).grid(row=1,column=1)
		Checkbutton(self.inputFrame,text='Show Plot',variable=self.showPlot_var).grid(row=2,column=1)
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

