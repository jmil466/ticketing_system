import pandas as pd
from tkinter import *

df = pd.read_csv("userlist.csv")
IDs = df.set_index("ID")

root = Tk()
inputID = Entry(root)

userID = 0
user = None

def confirm(event=None):
    """Creates a function to run the main function on keydown"""
    main()


def GUI():
    """Creates the GUI Window"""
    root.title("Ticketing System")
    root.geometry("400x200")
    label_ID = Label(root, text="Please Scan Your ID Card")
    label_ID.pack(fill=X)
    inputID.pack(fill=X)
    submit = Button(root, text="Submit", command=main)
    submit.pack(fill=X)
    root.bind('<Return>', confirm)


def main():
    """Checks all the user information to determine whether the user can enter 
    the ball"""
    global userID
    global user
    
    userID = inputID.get()
    inputID.delete(0, END)
    
    if userID.isdigit():
        userID = int(userID)
        if userID in df["ID"].tolist():
            user = User(userID)
            labelCreate("name")
            if user.has_ticket() == "yes":
                if user.in_ball() == 0:
                    IDs.loc[userID, "inBall"] = 1
                    IDs.to_csv("userlist.csv", index=True)
                    labelCreate("enter")
                elif user.in_ball() == 1:
                    labelCreate("inBall")
                else:
                    error(3)
            elif user.has_ticket() == "no":
                error(1)
            else:
                error(3)             
            
        elif userID not in df["ID"].tolist():
            error(2)
        else:    
            labelCreate("userError")            
    else:
        labelCreate("notNumber")            
    

class User:
    """Creates an object for the user of the ID being scanned, and allows the 
    returning of values from the specified CSV File"""
    
    df = pd.read_csv("userlist.csv")
    IDs = df.set_index("ID")    
    
    def __init__(self, userID):
        """Initalises the user class"""
        self.__id = userID
        self.__name = IDs.loc[userID, "name"]
        self.__ticket = IDs.loc[userID, "ticket"]
        self.__inBall = IDs.loc[userID, "inBall"]
        
        
    def getName(self):
        """Returns the users name"""
        return self.__name
        
        
    def getID(self):
        """Returns the users ID Number"""
        return self.__id
    
    
    def has_ticket(self):
        """Returns whether the user has a ticket"""
        return self.__ticket
    
    
    def in_ball(self):
        """Returns whether the user is already in the ball (Is used to prevent
        a users ticket being used twice"""
        return self.__inBall

def error (reason):
    """Function that outputs reason for entry denial"""
    if reason == 1:
        print("You do not have a ball ticket. Entry is denied")
        labelCreate("noTicket")
        labelCreate("name")
    elif reason == 2: 
        print("You are not registered in the system. Entry is denied")
        labelCreate("noUser")
    else:
        print("System Error! Please Scan again")
        labelCreate("error")    


def labelCreate(action):
    """Adds text to the GUI, sets the text to a specific value, 
    dependent on what has occurred"""
    
    #Sets the variables to be string variables, and makes their values "" (invisible")
    stringName = StringVar()
    stringTicket = StringVar()
    stringAction = StringVar() 
    
    printName = Label(root, textvariable=stringName)
    printName.place(x=132, y=95)    
    carPass = Label(root, textvariable=stringTicket)
    carPass.place(x=132, y=117)     
    position = Label(root, textvariable=stringAction)
    position.place(x=132, y=139)
    
    destroyTime = 2000  
    
    if action == "name":
        stringName.set(" Welcome " + user.getName().split(' ', 1)[0])
        root.after(destroyTime, printName.destroy)
    elif action == "noUser":
        stringName.set("User not found, see a staff member")
        root.after(destroyTime, printName.destroy)
    elif action == "noTicket":
        stringTicket.set("You don't have a ticket, see a staff member")
        root.after(destroyTime, carPass.destroy) 
    elif action == "enter":
        stringAction.set("Welcome to the ball!")
        root.after(destroyTime, position.destroy)
    elif action == "inBall":
        stringAction.set("You've already entered the ball, see a staff member")
        root.after(destroyTime, position.destroy)        
    elif action == "idEntry":
        stringName.set(" Error, Please Scan Again")
        root.after(destroyTime, printName.destroy)
    elif action == "notNumber":
        stringName.set("Error, Please Scan Your ID")  
        root.after(destroyTime, printName.destroy)     
    elif action == "error":
        stringAction.set("Error occured, please scan your ID again")
        root.after(destroyTime, position.destroy)  

GUI()

root.mainloop()
