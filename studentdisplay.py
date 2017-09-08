file = open("fullnames.txt")
import os,datetime,time
names = file.readlines()
import sqlite3 as sql
if not os.path.exists("./schoolSystem.db"):
    conn = sql.connect("schoolSystem.db")
    print("Creating")
    c = conn.cursor()#
    c.execute("""CREATE TABLE Students
    (id INTEGER PRIMARY KEY, firstName TEXT, lastName TEXT, state INTEGER)""")
    for name in names:
        name = name.split(" ")
        name = (None,name[0],name[-1][:-1],0)
        c.execute("""INSERT INTO Students VALUES (?,?,?,?)""",name)

    conn.commit()
    names = []
    for row in c.execute("SELECT * FROM Students"):
        print(row)
        names.append(str(row[0]))

    for n in names:
        c.execute("CREATE TABLE '%s' (date TEXT, outTime TEXT, inTime TEXT)" % n)
        conn.commit()
    print("Done creating")
def ohShit(ids):
    pass

def tap(conn,name):#a user has selected their name
    c = conn.cursor()
    name = name.title()
    name = tuple(name.split())
    ids = []
    for case in c.execute("SELECT state,id FROM Students WHERE firstName = ? AND lastName = ?",name):
        ids.append(case)
    ### now need to change the state and update the table
    if len(ids) > 1:
        student = ohshit(ids)
    else:
        student = ids[0]
    state = student[0]
    Sid = student[1]
    if state == 0:#student is leaving for lunch
        #change state in record
        #create new record in their personal table
        print(name,"is now out of the building")
        record = (datetime.datetime.strftime(datetime.date.today(),"%d-%m-%y"),datetime.datetime.strftime(datetime.datetime.now(),"%H-%M"),"Still logged out")
        c.execute("INSERT INTO '%s' VALUES (?,?,?)" % Sid,record)
    if state == 1:
        print("Welcome back",name)
        c.execute("UPDATE '%s' SET inTime=? WHERE date = ?" % Sid,(datetime.datetime.strftime(datetime.datetime.now(),"%H-%M"),datetime.datetime.strftime(datetime.date.today(),"%d-%m-%y")))
    state = not state
    c.execute("UPDATE Students SET state = ? WHERE id = ?",(state,Sid))
    conn.commit()
    
    conn.close()
conn = sql.connect("schoolSystem.db")
tap(conn,"scott harwood")
time.sleep(60)
conn = sql.connect("schoolSystem.db")
tap(conn,"scott harwood")
