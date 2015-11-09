from Tkinter import *
import pyReg
import getpass

courselist = []
user_name = None
password = None
alternate_pin = None
session = None
def signIn():
    global user_name, password, reg_pin, session
    user_name = raw_input("Enter your Colgate Username: ")
    password = getpass.getpass("Enter you Colgate account password: ")
    reg_pin = input("Enter your registration PIN: ")
    session = pyReg.reg_courses(user_name, password, reg_pin)

def whichSelected () :
    print "At %s of %d" % (select.curselection(), len(courselist))
    return int(select.curselection()[0])

def addEntry () :
    courselist.append ([regNumVar.get(), courseNameVar.get()])
    setSelect ()

def updateEntry() :
    courselist[whichSelected()] = [regNumVar.get(), courseNameVar.get()]
    setSelect ()

def deleteEntry() :
    del courselist[whichSelected()]
    setSelect ()

def loadEntry  () :
    regNum, courseName = courselist[whichSelected()]
    regNumVar.set(regNum)
    courseNameVar.set(courseName)
    print map(get_crn, courselist)
    
def setSelect () :
    courselist.sort()
    select.delete(0,END)
    for regNum,courseName in courselist :
        select.insert (END, (regNum, courseName))
        
def get_crn(c_entry):
	try:
		return int(c_entry[0])
	except:
		return c_entry[0]

def makeWindow () :
    global regNumVar, courseNameVar, select, regPINVar
    win = Tk()
    win.wm_title("Course registration: " + "mchavinda")
    win.geometry('{}x{}'.format(500, 450))
    frame1 = Frame(win, width = 500, height = 200)
    frame1.pack()
    Label(frame1, text="CRN").grid(row=0, column=0, sticky=W)
    regNumVar = StringVar()
    regNum = Entry(frame1, textvariable=regNumVar)
    regNum.grid(row=0, column=1, sticky=W)

    Label(frame1, text="Name").grid(row=1, column=0, sticky=W)
    courseNameVar= StringVar()
    courseName= Entry(frame1, textvariable=courseNameVar)
    courseName.grid(row=1, column=1, sticky=W)

    frame2 = Frame(win, width = 500, height = 200)       # Row of buttons
    frame2.pack()
    b1 = Button(frame2,text=" Add  ",command=addEntry)
    b2 = Button(frame2,text="Update",command=updateEntry)
    b3 = Button(frame2,text="Delete",command=deleteEntry)
    b4 = Button(frame2,text=" Load ",command=loadEntry)
    b1.pack(side=LEFT); b2.pack(side=LEFT)
    b3.pack(side=LEFT); b4.pack(side=LEFT)

    frame3 = Frame(win)       # select of regNums
    frame3.pack()
    scroll = Scrollbar(frame3, orient=VERTICAL)
    select = Listbox(frame3, yscrollcommand=scroll.set, height=20)
    scroll.config (command=select.yview)
    scroll.pack(side=RIGHT, fill=Y)
    select.pack(side=LEFT,  fill=BOTH, expand=1)
    return win
    

signIn()
win = makeWindow()
win.mainloop()

