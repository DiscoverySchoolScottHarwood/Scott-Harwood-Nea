import sqlite3 as sql
import tkinter as tk
USEDFONT = ("Andale Mono", 16)
NAMES = []
conn = sql.connect("schoolSystem.db")
c = conn.cursor()
count = 0
for row in c.execute("SELECT firstName,lastName FROM Students WHERE state = 0"):
    count +=1
    NAMES.append("{} {}".format(row[0],row[1]))
print(count)
#NAMES = NAMES[:20]
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
print(len(NAMES))
class slider():

    def __init__(self,data,master,x,y,height):
        self.x,self.y = x,y
        self.data = data
        self.rowHeight = 2
        self.master = master
        maxW = getMaxwidth(data)
        print(maxW)
        self.maxWidth = len(maxW)
        self.divider = self.rowHeight * USEDFONT[1] * 2
        self.displayed = int(SCREENHEIGHT / self.divider)#the number of elements in the list that is displayed on the screen
        self.slider = tk.Scale(master, from_ = 0, to = (len(data)-self.displayed), length = height,command = self.sliderChanged)
        self.slider.grid(row = y,column = x+1,rowspan = self.displayed) # a list of all currently displated Buttons
        self.genButtonslist(0,self.displayed)
        
    def genButtonslist(self,lr,ur):
        self.textButtons = []
        for i,name in enumerate(self.data[lr:ur]):
            button = tk.Button(self.master,text=name, font=USEDFONT, width=self.maxWidth,height=self.rowHeight, command=lambda:self.handleEntry(name))
            self.textButtons.append(button)
            button.grid(row = self.y+i,column = self.x)
    
    def handleEntry(self):
        pass

    def sliderChanged(self,*args):
        for x in self.textButtons:
            x.grid_forget()
        val = self.slider.get()
        self.genButtonslist(val, val+self.displayed)
        
class Main(tk.Frame):
    
    def __init__(self,master):
        super(Main,self).__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.slider = slider(NAMES,self,0,0,SCREENHEIGHT-50)
        self.slider2 = slider(NAMES,self,2,0,SCREENHEIGHT-50)

root = tk.Tk()
root.geometry("{}x{}".format(SCREENWIDTH,SCREENHEIGHT))
app = Main(root)

root.mainloop()
