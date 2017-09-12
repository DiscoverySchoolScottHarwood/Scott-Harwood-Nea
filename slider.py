import sqlite3 as sql
import tkinter as tk
USEDFONT = ("Andale Mono", 16)
NAMES = []
conn = sql.connect("schoolSystem.db")
c = conn.cursor()
for row in c.execute("SELECT firstName,lastName FROM Students WHERE state = 0"):
    NAMES.append("{} {}".format(row[0],row[1]))
NAMES = NAMES[:20]
SCREENHEIGHT = 480
SCREENWIDTH = 640
def sliderChanged(self):
        print(self.sliderval)

class slider():

    def __init__(self,data,master,x,y):
        self.data = data
        self.sliderVal = tk.IntVar
        rowHeight = 2
        self.slider = tk.Scale(master, from_ = 0, to = len(data)-1,variable = self.sliderVal)
        self.sliderVal.trace("w",sliderChanged)
        blank = tk.Button(master,text="",font=USEDFONT)
        self.displayed = int(SCREENHEIGHT / (rowHeight*USEDFONT[1]*2))#the number of elements in the list that is displayed on the screen
        self.slider.grid(row = y,column = x+1,rowspan = self.displayed)
        self.textFields = [] # a list of all currently displated Buttons
        self.sliderVal = tk.IntVar#the variable for the value of the slider

        for i,name in enumerate(self.data[:self.displayed]):
            button = tk.Button(master,text=name, font=USEDFONT, height=rowHeight, command=lambda:self.handleEntry(name))
            self.textFields.append(button)
            button.grid(row = y+i,column = x)
        


    def handleEntry(self,name):
        pass

class Main(tk.Frame):
    
    def __init__(self,master):
        super(Main,self).__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.slider = slider(NAMES,self,0,0)


root = tk.Tk()
root.geometry("{}x{}".format(SCREENWIDTH,SCREENHEIGHT))
app = Main(root)

root.mainloop()