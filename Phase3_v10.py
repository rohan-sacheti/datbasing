#Team 47
#Rohan Sacheti, Nija Kurien, Anirudh Reddy, Anmol Chhabria

from DB_Connect import *
import pymysql
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import urllib.request
import base64
from datetime import datetime
#from dateutil import parser
import random
import calendar
from collections import OrderedDict


class Train:
    def __init__(self,win):
        self.win=win
        self.win.title("Login")
        self.Login()

        #self.connect()
        #self.add_school('test2')
        self.file = DB_Connect()
        self.FinalUser=""
        self.FinalisStudent= 0
        self.isCustomer = 0
        self.isManager = 0


    def connect(self):
        try:
            self.db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
            user='cs4400_Team_47', passwd='GyckLuqf', db='cs4400_Team_47')
        except:
            print("Database connection error.")

    def Login(self):
        self.login = Frame(self.win)
        self.login.pack()

        Loginlabel = Label(self.login,text = "Login").grid(row = 0, column=0, columnspan = 5, sticky = EW)

        UnLabel = Label(self.login, text = "Username").grid(row=1, column = 0)
        self.un = StringVar()
        loginUN = Entry(self.login, textvariable = self.un, width = 30).grid(row=1, column =1, columnspan =4, sticky=EW)
        PwLabel = Label(self.login, text = "Password").grid(row=2,column =0)
        self.pw = StringVar()
        loginPW = Entry(self.login, textvariable = self.pw, show="*", width = 30).grid(row=2,column=1, columnspan=4, sticky = EW)
        loginBut = Button(self.login, text = "Login", command = self.LoginCheck).grid(row = 3, column =0, sticky = EW)
        loginButReg = Button(self.login, text = "Register", command = self.LogintoRegister).grid(row=3, column = 1, sticky = EW)

    def validate_user(self):
        db = self.connect()
        cursor = self.db.cursor()
        sqluser = """SELECT USERNAME FROM USER WHERE USERNAME = %s"""
        cursor.execute(sqluser, (username))
        resultuser = cursor.fetchall()
        #print(resultuser)


        sql = """SELECT PASSWORD FROM USER WHERE USERNAME = %s"""
        cursor.execute(sql, (username))
        result = cursor.fetchall()
        #print(result)
        #print(type(result))


    def LoginCheck(self):
        username = self.un.get()
        password = self.pw.get()

        result = self.file.validate_user(username, password)

        if username=="" or password=="":
            messagebox.showerror("Error", "Please enter a Username and Password.")
            return None
        elif result == None:
            messagebox.showerror("Error", "Incorrect username. Check username again or create an account.")
            return None
        elif result == 0:
            messagebox.showerror("Error", "Password does not match the Username.")
            return None
        elif result == 1:
            #print("working")
            self.FinalUser = self.un.get()

        self.isCustomer = self.file.is_Customer(self.FinalUser)
        #print(self.file.is_Customer(self.FinalUser))
        self.isManager = self.file.is_Manager(self.FinalUser)
        #print(self.file.is_Manager(self.FinalUser))

        if(self.isCustomer == 1 and  self.isManager == 1):
            print("User cannot be customer and manager.")

        if(self.isCustomer):
            self.Login_CF()
        elif(self.isManager):
            self.Login_ManagerCF()


##    def is_Manager(self, username):
##        """
##        Return 1 if manager, 0 otherwise
##        """
##        cursor = self.db.cursor()
##        sql = "SELECT 1 FROM MANAGER WHERE Username = '%s'" % username
##        cursor = self.query(cursor, sql)[0]
##        return 0 if (cursor.fetchone() == None) else 1
##
##    def is_Customer(self, username):
##        """
##        Return 1 if customer, 0 otherwise
##        """
##        cursor = self.db.cursor()
##        sql = "SELECT 1 FROM CUSTOMER WHERE Username = '%s'" % username
##        cursor = self.query(cursor, sql)[0]
##        return 0 if (cursor.fetchone() == None) else 1

    def Registration(self):

        self.win2 = Toplevel()
        self.win2.title("Registration")

        self.reg = Frame(self.win2)
        self.reg.pack()

        regTitle = Label(self.reg, text = "New User Registration"). grid(row = 0, column=0, columnspan =5)
        registerLabel = Label(self.reg, text= "Username"). grid(row=1,column = 0, sticky =E)
        registerLabel1 = Label(self.reg , text = "Email Address"). grid(row =2, column=0, sticky= E)
        registerLabel2 = Label(self.reg, text = "Password"). grid(row=3, column=0, sticky=E)
        registerLabel3 = Label(self.reg, text="Confirm Password:"). grid(row=4, column=0, sticky=E)

        self.Username = StringVar()
        self.Email = StringVar()
        self.Password = StringVar()
        self.ConfirmPW = StringVar()

        UN_Entry = Entry(self.reg, textvariable = self.Username, width = 30).grid(row=1,column=1,columnspan=3,sticky=EW)
        Email_Entry = Entry(self.reg, textvariable = self.Email, width = 30).grid(row = 2, column=1, columnspan=3, sticky=EW)
        PW_Entry = Entry(self.reg, textvariable = self.Password, width = 30, show="*").grid(row = 3, column=1, columnspan=3, sticky=EW)
        ConfirmPW_Entry = Entry(self.reg, textvariable = self.ConfirmPW, width = 30, show="*").grid(row = 4, column=1, columnspan=3, sticky=EW)

        #check to see if constraints are met and give error messages accordingly
        CreateBut = Button(self.reg, text = "Create", command = self.CheckRegister).grid(row=5,column=1, sticky=EW)
        BackBut = Button(self.reg, text = "Back", command = self.RegistertoLogin).grid(row = 5, column =2, sticky= EW)


    def CheckRegister(self):

        if self.Username.get() =="":
            messagebox.showwarning("Username Error", "Please make sure to enter a Username.")
            return None
        elif self.Email.get()=="":
            messagebox.showwarning("Error","Please make sure to enter an Email.")
            return None
        elif self.Password.get()=="" or self.ConfirmPW.get()=="":
            messagebox.showwarning("Password Error", "Please make sure to enter a password.")
            return None
        elif self.Password.get() != self.ConfirmPW.get():
            messagebox.showwarning("Password Error", "Please make sure that both passwords match.")
            return None
        elif self.Email.get()=="" or self.Password.get()=="" or self.ConfirmPW.get()=="":
            messagebox.showwarning("Error","Please make sure to enter an Email and Password.")
            return None
        elif (self.file.username_available(self.Username.get())) == 0:
            messagebox.showwarning("Username Error", "This username already exists. Please select another username.")
            return None

        if(self.file.username_available(self.Username.get())):
            # TODO: self.file.email_available(self.Email.get()) and
           if ( self.Password.get() == self.ConfirmPW.get()):
                db = self.connect()
                cursor = self.db.cursor()
                user = self.Username.get()
                email = self.Email.get()
                pw = self.Password.get()
                student = 0
                self.FinalUser = self.Username.get()
                self.FinalisStudent = 0
                sql1 = "INSERT INTO USER (Username, Password) VALUES ('%s','%s')" % (user, pw)
                sql2 = "INSERT INTO CUSTOMER (Username, Email, isStudent) VALUES('%s','%s', '%d')" % (user, email, student)
                try:
                    cursor.execute(sql1)
                    cursor.execute(sql2)
                    messagebox.showwarning("Successful Registration!", "Thank you for registering with GT Train.You can continue to the GTTrain User Functionalities.")
                    self.CheckRegister_CF()

                except:
                    print("Error inserting user into database0.")

##    def username_available(self, username):
##        db = self.connect()
##        cursor = self.db.cursor()
##        sql = "SELECT USERNAME FROM USER"
##        cursor.execute(sql)
##        result = cursor.fetchall()
##        for item in result:
##            user = str(item[0])
##            if (user.lower() == username.lower()):
##                messagebox.showwarning("Username Error", "This username already exists. Please select another username.")
##                return 0
##        return 1

##    def email_available(self, email):
##        db = self.connect()
##        cursor = self.db.cursor()
##        sql = "SELECT EMAIL FROM CUSTOMER"
##        try:
##            cursor.execute(sql)
##            result = cursor.fetchall()
##            for item in result:
##                if ((item[0]).lower() == email.lower()):
##                    return 0
##            return 1
##        except:
##            print("Error querying database2.")

    def ChooseFunctionality(self):
        self.win3 = Toplevel()
        self.win3.title("Choose Functionality - Customer View")

        self.CF = Frame(self.win3)
        self.CF.pack()

        l1 = Label(self.CF, text = "Choose Functionality:").grid(row = 0, column = 0, columnspan = 2, sticky = EW)
        b1 = Button(self.CF, text = "View Train Schedule", command=self.CF_VTS).grid(row = 2, column = 0, columnspan =3, sticky=EW)
        b2 = Button(self.CF, text = "Make a New Reservation", command=self.CF_MNR).grid(row = 3, column = 0, columnspan =3, sticky=EW)
        b3 = Button(self.CF, text = "Update a New Reservation", command=self.CF_UR).grid(row = 4, column = 0, columnspan =3, sticky=EW)
        b4 = Button(self.CF, text = "Cancel a New Reservation", command=self.CF_CR).grid(row = 5, column = 0, columnspan =3, sticky=EW)
        b5 = Button(self.CF, text = "Give Review", command=self.CF_GR).grid(row = 6, column = 0, columnspan =3, sticky=EW)
        b6 = Button(self.CF, text = "Add School Information (Student Discount)", command=self.CF_ASI).grid(row = 7, column = 0, columnspan =3, sticky=EW)

    def RegistertoLogin(self):
        self.win2.withdraw()
        self.win = Toplevel()
        self.Login()
        self.win.deiconify()

    def CheckRegister_CF(self):
        self.win2.withdraw()
        self.ChooseFunctionality()
        self.win3.deiconify()

    def Login_CF(self):
        self.win.withdraw()
        self.ChooseFunctionality()
        self.win3.deiconify()

    def Login_ManagerCF(self):
        self.win.withdraw()
        self.ManagerChooseFunctionality()
        self.MCF.deiconify()

    def LogintoRegister(self):
        self.win.withdraw()
        self.Registration()
        self.win2.deiconify()

    def CF_VTS(self):
        self.win3.withdraw()
##        self.VTS.destroy()
##        self.VTS = Toplevel()
        self.ViewTrainSchedule()
        self.VTS.deiconify()

    def VTS_CF(self):
        self.VTS.withdraw()
##        self.win3.destroy()
##        self.win3 = Toplevel()
        self.ChooseFunctionality()
        self.win3.deiconify()

    def VTSO_VTS(self):
        self.VTSO.withdraw()
##        self.VTS.destroy()
##        self.VTS = Toplevel()
        self.ViewTrainSchedule()
        self.VTS.deiconify()

    def CF_MNR(self):
        self.win3.withdraw()
##        self.MNR.destroy()
##        self.MNR = Toplevel()
        self.MakeNewReservation()
        self.MNR.deiconify()

    def MNR_CF(self):
        self.MNR.withdraw()
##        self.win3.destroy()
##        self.win3 = Toplevel()
        self.ChooseFunctionality()
        self.win3.deiconify()

    def SD_ST(self):
        self.SD.withdraw()
##        self.MNR.destroy()
##        self.MNR = Toplevel()
        self.MakeNewReservation()
        self.MNR.deiconify()

    def SD_TI(self):
        self.SD.withdraw()
##        self.TI.destroy()
##        self.TI = Toplevel()
        self.TravelInfo()
        self.TI.deiconify()

    def TI_SD(self):
        self.TI.withdraw()
##        self.SD.destroy()
##        self.SD = Toplevel()
        self.SelectDeparture()
        self.SD.deiconify()

    def TI_MR1(self):
        self.TI.withdraw()
##        self.MR1.destroy()
##        self.MR1 = Toplevel()
        self.MakeR1()
        self.MR1.deiconify()

    #new####
    def MR1_ST(self):
        self.MR1.withdraw()
##        self.MNR.destroy()
##        self.MNR = Toplevel()
        self.TravelInfo()
        self.MNR.deiconify()

    def MR1_TI(self):
        self.MR1.withdraw()
##        self.TI.destroy()
##        self.TI= Toplevel()
        self.MakeNewReservation()
        self.TI.deiconify()

    def MR1_P_Info(self):
        self.MR1.withdraw()
        #self.P_Info.destroy()
        #self.P_Info= Toplevel()
        self.Payment_Info()
        self.P_Info.deiconify()

    def P_Info_MR1(self):
        self.P_Info.withdraw()
        #self.P_Info.destroy()
        #self.P_Info= Toplevel()
        self.MakeR1()
        self.MR1.deiconify()

    def CF_UR(self):
        self.win3.withdraw()
        #self.UR.destroy()
        #self.UR = Toplevel()
        self.UpdateReservation()
        self.UR.deiconify()

    def UR_UR1(self):
        self.UR.withdraw()
        self.UpdateReservationOriginal()
        self.UR1.deiconify()

    def UR1_UR(self):
        self.UR1.withdraw()
        self.UpdateReservation()
        self.UR.deiconify()

    def UR_CF(self):
        self.UR.withdraw()
        #self.CF.destroy()
        #self.CF = Toplevel()
        self.ChooseFunctionality()
        self.CF.deiconify()

    def CF_CR(self):
        self.win3.withdraw()
        #self.CR.destroy()
        #self.CR = Toplevel()
        self.CancelReservation()
        self.CR.deiconify()

    def CF_GR(self):
        self.win3.withdraw()
        #self.GR.destroy()
        #self.GR = Toplevel()
        self.GiveReview()
        self.GR.deiconify()

    def CF_ASI(self):
        self.win3.withdraw()
        #self.ASI.destroy()
        #self.ASI = Toplevel()
        self.AddSchoolInformation()
        self.ASI.deiconify()

    def ASI_CF(self):
        self.ASI.withdraw()
        #self.win3.destroy()
        #self.win3 = Toplevel()
        self.ChooseFunctionality()
        self.win3.deiconify()

    def VRR_MCF(self):
        self.VRR.withdraw()
        self.ViewRevenueR()
        self.MCF.deiconify()

    def PRR_MCF(self):
        self.PRR.withdraw()
        self.ManagerChooseFunctionality()
        self.MCF.deiconify()


    def AddSchoolInformation(self):
        self.ASI = Toplevel()
        self.ASI.title("Add School Information")

        self.ASIf = Frame(self.ASI)
        self.ASIf.pack()

        self.EduEmail = StringVar()

        e1 = Entry(self.ASIf, textvariable = self.EduEmail, width = 30).grid(row=3,column=1,columnspan=3,sticky=EW)

        l1 = Label(self.ASIf, text = "Add School Info").grid(row = 1, column = 0, columnspan = 2, sticky = EW)
        l2 = Label(self.ASIf, text = "School Email Address").grid(row = 3, column = 0, sticky = EW)
        l3 = Label(self.ASIf, text = "Your school email address ends with .edu").grid(row = 5, column = 0, columnspan = 2, sticky = EW)

        b1 = Button(self.ASIf, text = "Back", command = self.ASI_CF).grid(row = 7, column = 0, columnspan = 2, sticky = W)
        b2 = Button(self.ASIf, text = "Submit", command = self.CheckEduEmail).grid(row = 7, column = 0, columnspan = 2, sticky = E)

    def CheckEduEmail(self):
        text = self.EduEmail.get()
        if text[-4:] == ".edu":
            self.file.add_school(self.Username.get())
            self.isStudent = 1
            self.ASI_CF()
        else:
            messagebox.showwarning("Student Email Error", "Your email does not end in .edu. Please make sure to enter a student email to qualify for discount.")

##    def add_school(self, username):
##        """
##        Sets isStudent field in customer entry
##        """
##        db = self.connect()
##        cursor = self.db.cursor()
##        sql = "UPDATE CUSTOMER SET isStudent = 1 WHERE USERNAME = \'" + username + '\''
##        try:
##            cursor.execute(sql)
##        except:
##            print("Error querying database.")

    def ViewTrainSchedule(self):
        self.VTS = Toplevel()
        self.VTS.title("View Train Schedule")

        self.VTSf = Frame(self.VTS)
        self.VTSf.pack()

        self.TrainNumber = StringVar()

        e1 = Entry(self.VTSf, textvariable = self.TrainNumber, width = 30).grid(row = 2, column = 1, sticky= E)

        l1 = Label(self.VTSf, text = "View Train Schedule").grid(row = 1, column = 0, columnspan = 5, sticky = EW)
        l2 = Label(self.VTSf, text = "Train Number"). grid(row = 2, column = 0, sticky = E)

        b1 = Button(self.VTSf, text = "Search", command=self.VerifyTrain).grid(row=5, column =0, sticky=EW)
        b2 = Button(self.VTSf, text = "Back to Functionalities", command = self.VTS_CF).grid(row=5, column = 1, sticky=EW)

    def VerifyTrain(self):
        train = self.TrainNumber.get()
        db = self.connect()
        cursor = self.db.cursor()
        sql = "SELECT DISTINCT TRAIN_NO FROM STOP WHERE TRAIN_NO = %s"
        cursor.execute(sql, (train))
        result = cursor.fetchall()

        if (result == ()):
            messagebox.showwarning("Train Results", "There are no current results for this train number. Please try a valid Train Number.")

        else:
            self.ViewTrainScheduleOptions()

    def ViewTrainScheduleOptions(self):

        train = self.TrainNumber.get()

        self.VTS.withdraw()
        self.VTSO = Toplevel()
        self.VTSO.title("View Train Schedule Options")
        self.VTSO.deiconify()
        frame = Frame(self.VTSO)
        frame.pack()

        tree = self.getTrainTree(frame)

        result = self.file.search_train_schedule(self.TrainNumber.get())
        #print(result)
        inc = 0
        for i in result:
            tree.insert('', inc, text='', values = i)
            inc = inc + 1

        b1 = Button(frame, text = "Back", command = self.VTSO_VTS).pack(side=BOTTOM)

##    def search_train_schedule(self, train_no):
##        """
##        Searches for a train, returns schedule if train found, None otherwise
##        Schedule is formatted as a list of tuples
##        The format for the tuple is (Name, Arrival_Time, Departure_Time)
##        """
##
##        cursor = self.db.cursor();
##        sql = "SELECT TRAIN_NO, Arrival_Time, Departure_Time, Name FROM STOP WHERE TRAIN_NO = " + str(train_no)
##        #print (sql)
##        try:
##            cursor.execute(sql)
##            result = cursor.fetchall()
##            return (None if (result == ()) else result)
##
##        except:
##            print("Error querying database.")


    def getTrainTree(self,frame):
        tree = Treeview(frame)
        tree.pack()

        tree["show"] = "headings"
        tree["columns"] = ("TNO","Arr","Dep","FCP","SCP")
        tree.heading("TNO", text = "Train (Train Number)")
        tree.heading("Arr",text = "Arrival Time")
        tree.heading("Dep", text="Departure Time")
        tree.heading("FCP",text="First Class Price")
        tree.heading("SCP",text="Second Class Price")

        return tree

    def MakeNewReservation(self):
        self.MNR = Toplevel()
        self.MNR.title("Make a New Reservation")

        frame = Frame(self.MNR)
        frame.pack()
        L0 = Label(frame,text = "Search Train").grid(row=0, column =0, sticky = EW)
        L1 = Label(frame,text = "Departs From").grid(row =1, column=0,sticky=E)
        L2 = Label(frame, text = "Arrives At").grid(row = 2, column =0 , sticky = E)
        L3 = Label(frame, text = "Departure Date (mm/dd/yyyy)").grid(row = 3, column =0 , sticky = E)

        #Run SQL code to get all the cities
        self.Cities = self.file.list_stations()
        self.depDD = StringVar()
        self.depDD.set(self.Cities[0])
        depDD = OptionMenu(frame, self.depDD, *self.Cities).grid(row=1,column=1, sticky = EW)

        #Run SQL code to get cities once again
        self.arrDD = StringVar()
        self.arrDD.set(self.Cities[0])
        arrDD = OptionMenu(frame, self.arrDD, *self.Cities).grid(row=2,column=1, sticky = EW)

        #self.DepDate = StringVar()
        #DepDate = Label(frame, text="Departure Date (MM/DD/YYYY)")
        self.DepDate = StringVar()
        #Add calendar icon
        E_DepDate = Entry(frame, textvariable = self.DepDate, width = 30).grid(row=3,column=1,columnspan=3,sticky=EW)


        b1 = Button(frame, text = "Find Trains", command = self.CheckDetails).grid(row = 4, column =0, sticky = EW)
        b2 = Button(frame, text = "Back to Functionalities", command = self.MNR_CF).grid(row =4, column = 1, sticky=EW)

##    def list_stations(self):
##        """
##        Returns a list of stations
##        """
##
##        cursor = self.db.cursor();
##        sql = "SELECT NAME, LOCATION FROM STATION"
##        try:
##            cursor.execute(sql)
##            result = cursor.fetchall()
##            stations = []
##            for row in result:
##                stations.append(row[0] + "(" + row[1] + ")")
##            return stations
##
##        except:
##            print("Error querying database.")

    def CheckDetails(self):


        DStation = self.depDD.get()
        AStation = self.arrDD.get()
        E_Date = self.DepDate.get()


        if DStation =="" or AStation == "":
            messagebox.showerror("Station Error", "Please select Departure/Arrival Station.")
            return None
        elif E_Date =="":
            messagebox.showerror("Date Error", "Please enter a Date.")
            return None
        elif DStation == AStation:
            messagebox.showerror("Station Error", "Departure and Arrival station is the same.")
            return None

        try:
            Date = datetime.strptime(E_Date, '%m/%d/%Y')
        except:
            messagebox.showerror("Date Error", "Date is invalid.")
            return None

        if Date < datetime.now():
            messagebox.showerror("Date Error", "Departure date has already passed.")
            return None

        print(DStation)
        print(AStation)

        search = self.file.select_departure(DStation, AStation)
        print(search)
        inc = 0

        if len(search) ==0:
            messagebox.showwarning("Reservation Error", "There are no results for this Departure and Arrival Station.")
            return None

        self.SelectDeparture()

    def SelectDeparture(self):

        DStation = self.depDD.get()
        AStation = self.arrDD.get()

        search = self.file.select_departure(DStation, AStation)
        print(search)

        self.SD =Toplevel()
        self.SD.title("Select Departure")

        frame = Frame(self.SD)
        frame.pack()
        print(start)

        Label(frame, text ="Train (Train Number)", relief ="raised").grid(row = 0, column = 0, sticky=EW)
        Label(frame, text ="Arrival Time", relief ="raised").grid(row = 0, column = 1, sticky=EW)
        Label(frame, text ="Departure Time", relief ="raised").grid(row = 0, column = 2, sticky=EW)
        Label(frame, text ="First Class Price", relief ="raised").grid(row = 0, column = 3, sticky=EW)
        Label(frame, text ="Second Class Price", relief ="raised").grid(row = 0, column = 4, sticky=EW)

        inc = 0

        print (search)
        for i in search:
            self.v = IntVar()
            Label(frame, text =i[0]).grid(row = inc + 1, column = 0, sticky =EW)
            Label(frame, text =i[2]).grid(row = inc + 1, column = 1, sticky =EW)
            Label(frame, text =i[1]).grid(row = inc + 1, column = 2, sticky = EW)
            Radiobutton(frame, text =str(i[3]), variable = self.v, value = (2*inc)).grid(row = inc + 1, column = 3)
            Radiobutton(frame, text =str(i[4]), variable = self.v, value = inc + 1).grid(row = inc + 1, column = 4)
            inc = inc + 1
        #error with date format
##        E_Date = self.DepDate.get()

        self.MNR.withdraw()
        self.SD.deiconify()

        b1 = Button(frame, text = "Back", command = self.SD_ST).pack(side=BOTTOM)
        b2 = Button(frame, text = "Next", command = self.SD_TI).pack(side=BOTTOM)

    #WHERE TO CALL

##    def select_departure(self, departure_station, arrival_station):
##        """
##        Return value is a list of tuples, and the tuple format is (train no, dep. time, arrival time)
##        """
##
##        #first, query for trains and their departure times that depart from departure station
##        cursor = self.db.cursor()
##        sql = "SELECT TRAIN_NO, DEPARTURE_TIME FROM STOP WHERE name='%s'" % departure_station
##        cursor = self.query(cursor, sql)[0]
##        dep_stas = cursor.fetchall()
##
##        listy_list = []
##        temp = []
##
##        for i in dep_stas:
##            #using those trains we queried, find those that arrive at arrival station at a later time
##            sql = "SELECT TRAIN_NO FROM STOP WHERE name='%s' AND TRAIN_NO='%d' AND ARRIVAL_TIME > '%s'" % (arrival_station, i[0], i[1])
##            cursor = self.query(cursor, sql)[0]
##            temp.append(cursor.fetchone())
##
##        for j in temp:
##            if (j):
##                #get the departure time from those trains
##                sql = "SELECT DEPARTURE_TIME FROM STOP WHERE Train_No='%d' AND Name='%s'" % (j[0], departure_station)
##                cursor = self.query(cursor, sql)[0]
##                dep_t = (cursor.fetchone())[0]
##                #get the arrival time from those trains
##                sql = "SELECT ARRIVAL_TIME FROM STOP WHERE Train_No='%d' AND Name='%s'" % (j[0], arrival_station)
##                cursor = self.query(cursor, sql)[0]
##                arr_t = (cursor.fetchone())[0]
##                listy_list.append((j[0],dep_t,arr_t))
##
##        return listy_list

    def getDepartureTree(self,frame):
        tree = Treeview(frame)
        tree.pack()

        tree["show"] = "headings"
        tree["columns"] = ("TNO","Time","first","second")
        tree.heading("TNO", text = "Train (Train Number)")
        tree.heading("Time",text = "Time (Duration)")
        tree.heading("first", text="1st Class Price")
        tree.heading("second",text="2nd Class Price")

        return tree

    def TravelInfo(self):
        self.TI = Toplevel()
        self.TI.title("Travel Extras & Passenger Info")

        frame = Frame(self.TI)
        frame.pack()

        L0 = Label(frame, text="Travel Extras & Passenger Info").grid(row = 0, column=0, sticky = EW)
        L1 = Label(frame, text = "Number of Baggage").grid(row=1,column=0, sticky =EW)
        L2 = Label(frame, text = "Every passenger can bring up to 4 baggage. 2 free of charge, 2 for $30 per bag").grid(row=2,column=0, sticky =EW)
        L3 = Label(frame, text = "Passenger Name").grid(row=3,column=0, sticky =EW)

        Num = [0,0,1,2,3,4]
        self.bag = IntVar()

        depDD = OptionMenu(frame, self.bag, *Num).grid(row=1,column=1, sticky = W)

        PName = StringVar()
        self.PName=Entry(frame,textvariable = PName,width=30).grid(row =3, column = 1, sticky = W)

        b1 = Button(frame, text = "Back", command = self.TI_SD).grid(row=4, column =1, sticky = EW)
        b2 = Button(frame, text = "Next", command = self.TI_MR1).grid(row=4,column=2,sticky=EW)


    def MakeR1(self):
        self.MR1 = Toplevel()
        self.MR1.title("Make Reservation")

        frame = Frame(self.MR1)
        frame.pack()

        L0= Label(frame, text = "Currently Selected").pack()
        tree = self.getMakeR1Tree(frame)

        TrainInfo = [("2222 express", "12:30", "Boston", "Atl", "2nd", "$115","3","Alier Hu", "Add Remove Button"),("2222", "12:30", "3:30", "chichi")] #test points
        self.TrainList = []

        inc = 0
        for i in TrainInfo:
            tree.insert('', inc, text='', values = i)
            #removeButton=ResSelected(frame,text="Remove", onvalue=1, offvalue=0).pack(side=RIGHT)
            inc = inc + 1
            self.TrainList.append(i)


        frame2 = Frame(self.MR1)
        frame2.pack()
        Label(frame2, text = "Student Discount Applied").grid(row=0,column=0,sticky = EW)
        Label(frame2, text = "Total Cost").grid(row=1,column=0,sticky = E)
        self.cost = "134" #update with SQL statements
        Entry(frame2, textvariable = self.cost, width = 20).grid(row=1,column=1,sticky = E)

        Label(frame2, text="Use Card").grid(row=2,column=0,sticky=E)
        #SQL to get card numbers stored under passenger
        self.CardOptions = self.file.find_card(self.Username.get())
        self.cardDD = StringVar()
        self.cardDD.set(self.CardOptions[0])
        cardDD = OptionMenu(frame2, self.cardDD, *self.CardOptions).grid(row=2,column=1, sticky = EW)
        Button(frame2, text ="Add Card", command = self.PaymentInfo()).grid(row=2, column =2, sticky=EW)

        Button(frame2, text = "Continue adding a train", command = self.MR1_ST).grid(row=3,column=0,sticky=EW)
        Button(frame2, text="Back",command = self.MR1_TI).grid(row=4,column=0, sticky=EW)
        Button(frame2,text="Submit",command = self.MR1_P_Info).grid(row=4,column=1,sticky=EW)

##    def find_card(self, username):
##        cursor = self.db.cursor()
##        sql = "SELECT CARD_NUMBER FROM PAYMENT_INFO WHERE CARD_USERNAME='%d'" % username
##        try:
##            cursor.execute(sql)
##        except :
##            e = sys.exc_info()
##            print (e)
##            print("Error, querying the database")
##        listy_list = []
##        temp = cursor.fetchone()
##        while temp:
##            listy_list.append(temp[0])
##            temp = (cursor.fetchone() %10000)
##        return listy_list


    #WHERE TO CALL
##    def make_reservation(self, username, card_number):
##        cursor = self.db.cursor()
##        sql = "INSERT INTO RESERVATION (CARD_NO, USERNAME, IS_CANCELLED) VALUES ('%d', '%s', '0')" % (card_number, username)
##        try:
##            cursor.execute(sql)
##        except :
##            e = sys.exc_info()
##            print (e)
##            print("Error, querying the database")


    def getMakeR1Tree(self,frame):
        tree = Treeview(frame)
        tree.pack()

        tree["show"] = "headings"
        tree["columns"] = ("TNO","Time","D","A","Class","Price","Bag","PName","Remove")
        tree.heading("TNO", text = "Train (Train Number)")
        tree.heading("Time",text = "Time (Duration)")
        tree.heading("D", text="Departs From")
        tree.heading("A",text="Arrives At")
        tree.heading("Class", text = "Class")
        tree.heading("Price",text = "Price")
        tree.heading("Bag", text="# of Baggages")
        tree.heading("PName",text="Passenger Name")
        tree.heading("Remove",text="Remove")


        return tree

    def Payment_Info(self):
        self.P_Info = Toplevel()
        self.P_Info.title("Payment Information")

        frame = Frame(self.P_Info)
        frame.pack()

        Label(frame, text="Payment Information").grid(row=0,column=0,sticky=E)
        Label(frame,text= "Add Card").grid(row=1,column=0,sticky=E)

        Label(frame,text="Name on Card").grid(row=2,column=0,sticky=E)
        self.name=StringVar()
        Entry(frame,textvariable=self.name,width=20).grid(row=2,column=1,sticky=E)

        Label(frame,text="Card Number").grid(row=3,column=0,sticky=E)
        self.ccNo = StringVar()
        Entry(frame,textvariable = self.ccNo, width=20).grid(row=3,column=1,sticky=E)

        Label(frame,text="CVV").grid(row=4,column=0,sticky=E)
        self.cvv=IntVar()
        Entry(frame,textvariable=self.cvv,width=20).grid(row=4,column=1,sticky=E)

        Label(frame,text="Expiration Date").grid(row=5,column=0,sticky=E) ##Date picker
        self.eDate=StringVar() #Date format
        Entry(farme,textvariable=self.eDate,width=20).grid(row=5,column=1,sticky=E)


        Label(frame,text="Delete Card").grid(row=1,column=3,sticky=W)
        Label(frame, text="Card Number").grid(row=2,column=3,sticky=W)

        cardDrop = OptionMenu(frame2, self.cardDD, *self.CardOptions).grid(row=2,column=4, sticky = EW)
        addB=Button(frame,text="Submit",command=self.addCardCheck).grid(row=7,column=0,sticky=EW)
        delB=Button(frame,text="Submit",command=self.delCardCheck).grid(row=7,column=3,sticky=EW)

    def addCardCheck(self):
        if self.eDate.get() > datetime.now():
            self.P_Info_MR1()
            self.file.add_card()
        else:
            messagebox.showerror("Expiration Date Error", "Card has expired.")

    def delCardCheck(self):
        ##ADD SQL STATEMENTS to delete card from database
        self.P_Info_MR1()


    def UpdateReservation(self):
        self.UR = Toplevel()
        self.UR.title("Update Reservation")

        frame = Frame(self.UR)
        frame.pack()

        self.resID = IntVar()
        ridNum =self.resID.get()

        l0 = Label(frame, text = "Update Reservation").grid(row = 0, column =0, columnspan=5, sticky=EW)
        l1 = Label(frame, text = "Reservation ID").grid(row = 1, column = 0, sticky= EW)
        e1 = Entry(frame, textvariable = self.resID, width = 30).grid(row = 1, column = 1, sticky = EW)
        b1 = Button(frame, text = "Search", command = self.URCheck).grid(row = 1, column=2, sticky = EW)
        b2 = Button(frame, text = "Back", command = self.UR_CF).grid(row = 4, column =0, columnspan = 5, sticky=EW)


    def URCheck(self):

        ridNum = self.resID.get()

        if ridNum == "":
            messagebox.showerror("Reservation ID Error", "Please make sure to enter a Reservation ID.")
            return None
        elif self.file.validate_res_id(self.resID.get()) == None:
            messagebox.showerror("Reservation ID Error", "Reservation ID is invalid.")
            return None
        elif self.file.validate_res_id(self.resID.get()) == 1:
            self.UR_UR1()

    def UpdateReservationOriginal(self):
        self.UR1 = Toplevel()
        self.UR1.title("Update Reservation")

        frame = Frame(self.UR1)
        frame.pack()

        self.UR.withdraw()
        self.UR1.deiconify()

        tree = self.getURTree(frame)
        ridNum =self.resID.get()

        #result = self.file.get_train_tickets(ridNum)
        result = [("24", '1', '04-14-2016', 'Anie', '3', 'lolol', 'Norfolk', '232', '2323', '2323')]
        print(len(result))
        inc = 0
        self.v = IntVar()
        #(Train_No, Class, Dep_Date, Pass_Name, Num_Bags, Dep_From, Arr_At, Dep_Time, Arr_Time, Class_Price)

        for i in result:
            rb1 = Radiobutton(frame, text ="Select", variable= self.v, value = inc + 1)
            tree.insert('', inc, text='', values = (Radiobutton(frame, text ="Select", variable= self.v, value = inc + 1), i[0], i[2], i[5], i[6], i[1], i[9], i[4], i[3]))
            inc = inc + 1

        self.v.set(-1)
        b1 = Button(frame, text = "Back", command = self.UR1_UR).pack(side=BOTTOM)


        pass

    def getURTree(self, frame):
        tree = Treeview(frame)
        tree.pack()

        tree["show"] = "headings"
        tree["columns"] = ("Select", "TNO","Time","D","A","Class","Price","Bag","PName")
        tree.heading("Select", text= "Select")
        tree.heading("TNO", text = "Train (Train Number)")
        tree.heading("Time",text = "Time (Duration)")
        tree.heading("D", text="Departs From")
        tree.heading("A",text="Arrives At")
        tree.heading("Class", text = "Class")
        tree.heading("Price",text = "Price")
        tree.heading("Bag", text="# of Baggages")
        tree.heading("PName",text="Passenger Name")

        return tree


    def UpdateReservationNew(self):
        self.UR2 = Toplevel()
        self.UR2.title("Update Reservation")

        frame = Frame(self.UR2)
        frame.pack()

        l0 = Label(frame, text ="Current Train Ticket").grid(row = 0, column = 0, sticky = E)

        ridNum =self.v.get()

        tree1 = self.getURTree(frame)
        i = result[ridNum]
        self.dd= i[2]
        rb1 = Radiobutton(frame, text ="Select", variable= self.v, value = inc)
        tree1.insert('', inc, text='', values = (rb1, i[0], i[2], i[5], i[6], i[1], i[9], i[4], i[3]))
        inc = inc + 1

        self.DeptDate = StringVar()

        l1 = Label(frame, text = "New Departure Date").grid(row = 4, column =0, sticky = E)
        e1 = Entry(frame, textvariable = self.DeptDate, width = 30).grid(row =4, column = 1, sticky = EW)
        b1 = Button(frame, text ="Search Availability", command= self.UpdateSearchCheck).grid(row = 4, column = 3, sticky=EW)

    def UpdateSearchCheck(self):

        if self.DeptDate >= date.datetime.now():
            messagebox.showwarning("Update Error", "")

    def CancelReservation(self):
        self.CR = Toplevel()
        self.CR.title("Cancel Reservation")

        frame = Frame(self.CR)
        frame.pack()

        l0

        pass


    def getCRTree(self, frame):
        tree = Treeview(frame)
        tree.pack()

        tree["show"] = "headings"
        tree["columns"] = ("TNO","Time","D","A","Class","Price","Bag","PName")
        tree.heading("TNO", text = "Train (Train Number)")
        tree.heading("Time",text = "Time (Duration)")
        tree.heading("D", text="Departs From")
        tree.heading("A",text="Arrives At")
        tree.heading("Class", text = "Class")
        tree.heading("Price",text = "Price")
        tree.heading("Bag", text="# of Baggages")
        tree.heading("PName",text="Passenger Name")


    def GiveReview(self):
        self.GR = Toplevel()
        self.GR.title("Give Review")

        frame = Frame(self.GR)
        frame.pack()

        self.TrainNum = StringVar()
        self.Comment = StringVar()

        l0 = Label(frame, text = "Give Review").grid(row = 0, column = 0, columnspan = 2, sticky = EW)
        l1 = Label(frame, text = "Train Number").grid(row=1, column=0, sticky=EW)
        e1 = Entry(frame, textvariable = self.TrainNum, width =30).grid(row = 1, column = 2, sticky=EW)

        l2 = Label(frame, text = "Rating").grid(row =2, column = 0, sticky=EW)

        l3 = Label(frame, text = "Comment").grid(row =3, column =0, sticky = EW)
        e2 = Entry(frame, textvariable = self.Comment, width = 30).grid(row = 3, column = 2, sticky = EW)

        b1 = Button(frame, text = "Submit", command = self.GiveReviewCheck).grid(row = 5, column = 1, sticky = E)

    def GiveReviewCheck (self):

        review = self.Comment.get()
        train = self.TrainNum.get()

        #checktrainexistingnumber
        if train not in data:
            messagebox.showerror("Error", "Please enter a valid train number.")
        if review =="":
            messagebox.showerror("Error", "Please enter something in the Comment box to record a review")

    def ManagerChooseFunctionality(self):

        self.MCF = Toplevel()
        self.MCF.title("Choose Functionality - Manager View")

        frame = Frame(self.MCF)
        frame.pack()

        l0 = Label(frame, text = "Choose Functionality").grid(row = 0, column = 0, columnspan = 2, sticky=EW)
        b1 = Button(frame, text = "View Revenue Report", command = self.ViewRevenueR).grid(row = 2, column = 0, columnspan = 2, sticky=EW)
        b2 = Button(frame, text = "View Popular Route Report", command = self.ViewPopularRR).grid(row= 4, column = 0, columnspan = 2, sticky=EW)


        b3 = Button(frame, text = "Log Out", command = self.LogOut).grid(row = 7, column = 2, sticky = W)


    def ViewRevenueR(self):

        self.VRR = Toplevel()
        self.VRR.title("View Revenue Report")

        self.MCF.withdraw()
        self.VRR.deiconify()
        frame = Frame(self.VRR)
        frame.pack()

        tree = self.getRReportTree(frame)

        result = self.file.revenue_report()
        #print(result)
        inc = 0
        for i in result:
            tree.insert('', inc, text='', values = i)
            inc = inc + 1

        b1 = Button(frame, text = "Back", command = self.VRR_MCF).pack(side=BOTTOM)


    def getRReportTree(self,frame):
        tree = Treeview(frame)
        tree.pack()

        tree["show"] = "headings"
        tree["columns"] = ("Month","Revenue")
        tree.heading("Month", text = "Month")
        tree.heading("Revenue",text = "Revenue")

        return tree

    def ViewPopularRR(self):
        self.PRR = Toplevel()
        self.PRR.title("View Popular Route Report")

        self.MCF.withdraw()
        self.PRR.deiconify()
        frame = Frame(self.PRR)
        frame.pack()

        tree = self.getViewPRRTree(frame)

        result = self.file.popular_report()

        inc = 0
        for i in result:
            tree.insert('', inc, text='', values = i)
            inc = inc + 1

        b1 = Button(frame, text = "Back", command = self.PRR_MCF).pack(side=BOTTOM)

    def getViewPRRTree(self, frame):

        tree = Treeview(frame)
        tree.pack()

        tree["show"] = "headings"
        tree["columns"] = ("Month","TrainNO", "NoRes")
        tree.heading("Month", text = "Month")
        tree.heading("TrainNO",text = "Train Number")
        tree.heading("NoRes", text = "#ofReservations")

        return tree

    def LogOut(self):
        self.MCF.destroy()

class UserSelected(Checkbutton):
    def __init__(self,*args,**chargs):
            self.var = IntVar()
            self.text = chargs['text']
            # self.roomtuple = None
            chargs['variable'] = self.var
            Checkbutton.__init__(self,*args,**chargs)

    def is_checked(self):
            return self.var.get()

    def toString(self):
            return self.text

root = Tk()
Train(root)
root.mainloop()
