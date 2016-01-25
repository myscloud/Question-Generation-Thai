import tkinter as tk

class simpleui(tk.Frame):

	def __init__(self, master=None):
		tk.Frame.__init__(self, master)
		self.pack()
		self.createWidgets()

	def createWidgets(self):
		pass

	
