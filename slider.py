import sqlite3 as sql
import tkinter as tk
import time
import datetime
USEDFONT = ("Andale Mono", 16)
#basic code to assemble data set
NAMES = []
conn = sql.connect("schoolSystem.db")
c = conn.cursor()

for row in c.execute("SELECT firstName,lastName FROM Students WHERE state = 0"):
    NAMES.append("{} {}".format(row[0],row[1]))

NAMES = NAMES[:20]
#/basic code to assemble data set

SCREENHEIGHT = 480
SCREENWIDTH = 700

def getMaxwidth(data):
    maxLen = 0
    val = None
    for x in data:
        if len(x) > maxLen:
            maxLen = len(x)
            val = x
    return val

class slider():

    def __init__(self,data,master,x,y,height):
        self.x,self.y = x,y
        self.data = data
        self.rowHeight = 2
        self.master = master
        self.maxWidth = len(getMaxwidth(data))
        self.divider = self.rowHeight * USEDFONT[1] * 2
        self.displayed = int(SCREENHEIGHT / self.divider)#the number of elements in the list that is displayed on the screen
        self.slider = tk.Scale(master, from_ = 0, to = (len(data)-self.displayed), length = height,command = self.sliderChanged)
        self.slider.grid(row = y,column = x+1,rowspan = self.displayed) # a list of all currently displated Buttons
        self.genButtonslist(0,self.displayed)

    def genButtonslist(self,lr,ur):
        self.textButtons = []
        for i,name in enumerate(self.data[lr:ur]):
            button = tk.Button(self.master,text=name, font=USEDFONT, width=self.maxWidth,height=self.rowHeight, command= lambda name=name: self.handleEntry(name))
            self.textButtons.append(button)
            button.grid(row = self.y+i,column = self.x)
    
    def handleEntry(self,name):
        n = name.split()
        print(n)
        for x in c.execute("SELECT id,state FROM Students WHERE firstName = ? AND lastName = ?",(n[0],n[1])):
            print(x)
            if x[1] == 1:
                print("Got here")
                c.execute("UPDATE '%s' SET inTime = ?" % x[0],(datetime.datetime.strftime(datetime.datetime.now(),"%H-%M"),))
                c.execute("UPDATE Students SET state = 0 WHERE id = ?",(x[0],))
            else:
                print("The other one")
                record = (datetime.datetime.strftime(datetime.date.today(),"%d-%m-%y"),datetime.datetime.strftime(datetime.datetime.now(),"%H-%M"),"Still logged out")
                c.execute("INSERT INTO '%s' VALUES (?,?,?)" % x[0],record)
                c.execute("UPDATE Students SET state = 1 WHERE firstName = ? AND lastName = ? AND state = 0",(n[0],n[1]))

        conn.commit()
    def sliderChanged(self,*args):
        for x in self.textButtons:
            x.grid_forget()
        val = self.slider.get()
        self.genButtonslist(val, val+self.displayed)

    def grid_forget(self):
        for x in self.textButtons:
            x.grid_forget()
        self.slider.grid_forget()
        
class Main(tk.Frame):
    
    def __init__(self,master):
        super(Main,self).__init__(master)
        self.grid()     
        self.state = 0
        data = []
        self.subframe = tk.Frame()
        self.subframe.grid()
        for row in c.execute("SELECT firstName,lastName FROM Students WHERE state = 0"):
            data.append("{} {}".format(row[0],row[1]))
        self.slider = slider(data,self.subframe,1,0,SCREENHEIGHT-200)
        self.createWidgets()
        self.in_button_pressed

    def createWidgets(self):
        self.OutB = tk.Button(self.master,text="Sign Out",font=USEDFONT,command = self.out_button_pressed)
        self.InB = tk.Button(self.master,text="Sign In",font=USEDFONT,command=self.in_button_pressed)
        self.OutB.grid(column=0,row=0)
        self.InB.grid(column=1,row=0)

    def out_button_pressed(self):
        print("button pressed")
        print(self.state)
        if self.state == 1:#is in sign in mode
            print()
            self.slider.grid_forget()
            data = []
            for row in c.execute("SELECT firstName,lastName FROM Students WHERE state = 0"):
                data.append("{} {}".format(row[0],row[1]))
            if len(data) > 0:
                self.slider = slider(data,self.subframe,1,0,SCREENHEIGHT-150)
                self.state = not self.state

    def in_button_pressed(self):
        print("In Button Pressed")
        print(self.state)
        if self.state == 0:
            self.slider.grid_forget()
            data = []
            for row in c.execute("SELECT firstName,lastName FROM Students WHERE state = 1"):
                data.append("{} {}".format(row[0],row[1]))
            if len(data) > 0:
                self.slider = slider(data,self.subframe,1,0,SCREENHEIGHT-200)
            self.state = not self.state


root = tk.Tk()
root.geometry("{}x{}".format(SCREENWIDTH,SCREENHEIGHT))
app = Main(root)

root.mainloop()
