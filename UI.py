from Tkinter import *
import pyReg
import getpass
import tkSimpleDialog

courselist = []
username = ""
password = None
reg_pin = None
courseList = []

class Login(tkSimpleDialog.Dialog):

    def body(self, master):
    #master.destroy()
        Label(master, text="Username:").grid(row=0)
        Label(master, text="Password:").grid(row=1)
        Label(master, text="PIN     :").grid(row=2)
        self.e1 = Entry(master)
        self.e2 = Entry(master, show="*")
        self.e3 = Entry(master)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
    #master.withdraw()
        return self.e1 # initial focus

    def apply(self):
        global username, password, reg_pin
        username = str(self.e1.get())
        password = str(self.e2.get())
        reg_pin = str(self.e3.get())
        return (username, password, reg_pin) # or something
        


def signIn():
    global username, password, reg_pin #, session
    root = Tk()
    root.wm_title("Course registration")
    root.geometry('{}x{}'.format(400, 150))
    root.withdraw()
    while True:
        login = Login(root)
        logged_in = False
        session, logged_in = pyReg.login_to_portal(username, password)
        if logged_in:
            break
    session = pyReg.login_to_banner(session)
    root.destroy()
    return session
    
def whichSelected () :
    print "At %s of %d" % (select.curselection(), len(courseList))
    return int(select.curselection()[0])

def addEntry () :
    courseList.append ([crnVar.get(), courseNameVar.get()])
    setSelect ()

def updateEntry() :
    courseList[whichSelected()] = [crnVar.get(), courseNameVar.get()]
    setSelect ()

def deleteEntry() :
    del courseList[whichSelected()]
    setSelect ()

def loadEntry  () :
    name, phone = courseList[whichSelected()]
    crnVar.set(name)
    courseNameVar.set(phone)

def sendData(session):
    sendlist = map(lambda s: s[0], courseList)
    return pyReg.reg_courses(session, sendlist, reg_pin)

def makeWindow (session) :
    global crnVar, courseNameVar, select
    win = Tk()
    win.resizable(width=FALSE, height=FALSE)
    win.wm_title("Course registration: " + username)
    frame1 = Frame(win)
    frame1.pack()

    Label(frame1, text="CRN").grid(row=0, column=0, sticky=W)
    crnVar = StringVar()
    name = Entry(frame1, textvariable=crnVar)
    name.grid(row=0, column=1, sticky=W)

    Label(frame1, text="Course Name").grid(row=1, column=0, sticky=W)
    courseNameVar= StringVar()
    phone= Entry(frame1, textvariable=courseNameVar)
    phone.grid(row=1, column=1, sticky=W)

    frame2 = Frame(win)       # Row of buttons
    frame2.pack()
    b1 = Button(frame2,text="     Add    ",command=addEntry)
    b2 = Button(frame2,text="   Update   ",command=updateEntry)
    b3 = Button(frame2,text="   Delete   ",command=deleteEntry)
    b4 = Button(frame2,text="    Load    ",command=loadEntry)
    b5 = Button(frame2,text=" Send Data  ",command=lambda: sendData(session))
    b1.pack(side=LEFT); b2.pack(side=LEFT)
    b3.pack(side=LEFT); b4.pack(side=LEFT)
    b5.pack(side=LEFT)
    frame3 = Frame(win)       # select of names
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=6)
    scroll.config (command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)
    return win

def setSelect () :
    courseList.sort()
    select.delete(0,END)
    for name,phone in courseList :
        select.insert (END, name)
session = signIn()
win = makeWindow(session)
setSelect ()
win.mainloop()
