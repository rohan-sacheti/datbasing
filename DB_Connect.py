import pymysql, sys
from datetime import date


#IMPORTANT: Make sure to set ON DELETE/ON UPDATE to CASCADE for those necessary

class DB_Connect:
    """ Provides methods to query database """

    def __init__(self):
        self.connect()


    def connect(self):
        try:
            self.db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
            user='cs4400_Team_47', password='GyckLuqf', db='cs4400_Team_47')
        except:
            print("Database connection error.")

    def create_user(self, username, password, email):
        """
        Precondition: username, password, and email are valid (not empty string, valid characters)
        """

        if(self.username_available(username)):
            cursor = self.db.cursor()
            sql1 = "INSERT INTO USER VALUES(\'" + username + '\',\'' + password + '\')'
            sql2 = "INSERT INTO CUSTOMER VALUES(\'" + username + '\',\'' + email + '\',' + '0)'
            self.query(cursor,sql1)
            self.query(cursor,sql2)
        else:
            print("Username not available.")

    def username_available(self, username):
        """
        Checks if username not taken in db
        """

        cursor = self.db.cursor()
        sql = "SELECT USERNAME FROM USER"
        cursor = self.query(cursor,sql)[0]
        result = cursor.fetchall()
        for user in result:
            if (user[0].lower() == username.lower()):
                return 0
        return 1

    def add_school(self, username):
        """
        Sets isStudent field in customer entry
        """

        cursor = self.db.cursor()
        sql = "UPDATE CUSTOMER SET isStudent = 1 WHERE USERNAME = \'" + username + '\''
        self.query(cursor, sql)

    def is_student(self, username):
        cursor = self.db.cursor()
        sql = "SELECT ISSTUDENT FROM CUSTOMER WHERE USERNAME = '%d'" % useranme
        self.query(cursor, sql)

    def validate_user(self, username, password):
        """
        Returns 1 if entered password equals pw in db, 0 if password does not match,
        None if user not in database
        """

        cursor = self.db.cursor()
        sql = "SELECT PASSWORD FROM USER WHERE Username = '%s'" % username
        cursor = self.query(cursor, sql)[0]
        result = cursor.fetchone()
        if (result): return (0 if (password != result[0]) else 1)
        else: return None

    def is_Manager(self, username):
        """
        Return 1 if manager, 0 otherwise
        """
        cursor = self.db.cursor()
        sql = "SELECT 1 FROM MANAGER WHERE Username = '%s'" % username
        cursor = self.query(cursor, sql)[0]
        return 0 if (cursor.fetchone() == None) else 1

    def is_Customer(self, username):
        """
        Return 1 if customer, 0 otherwise
        """
        cursor = self.db.cursor()
        sql = "SELECT 1 FROM CUSTOMER WHERE Username = '%s'" % username
        cursor = self.query(cursor, sql)[0]
        return 0 if (cursor.fetchone() == None) else 1


    def search_train_schedule(self, train_no):
        """
        Searches for a train, returns schedule if train found, None otherwise
        Schedule is formatted as a list of tuples
        The format for the tuple is (Train_No, Arrival_Time, Departure_Time, Name)
        """

        cursor = self.db.cursor();
        sql = "SELECT Train_No, Arrival_Time, Departure_Time, Name FROM STOP WHERE TRAIN_NO = " + str(train_no)
        cursor = self.query(cursor, sql)[0]
        result = cursor.fetchall()
        return (None if (result == ()) else result)

    def list_stations(self):
        """
        Returns a list of stations
        """

        cursor = self.db.cursor();
        sql = "SELECT NAME, Location FROM STATION"
        cursor = self.query(cursor, sql)[0]
        result = cursor.fetchall()
        stations = []
        for row in result:
            stations.append(row[0] + "(" + row[1] + ")")
        return stations

    def add_card(self, name_on_card, card_number, cvv, exp_date, username):
        cursor = self.db.cursor()
        sql = "INSERT INTO PAYMENT_INFO VALUES ('%d', '%s', '%s', '%d', '%s')" % (card_number, name_on_card, exp_date, cvv, username)
        cursor = self.query(cursor, sql)

    def delete_card(self, card_number):
        cursor = self.db.cusor()
        sql = "DELETE FROM PAYMENT_INFO WHERE CARD_NUMBER = '%d'" % card_number
        self.query(cursor, sql)

    #test
    def select_departure(self, departure_station, arrival_station):
        """
        Return value is a list of tuples, and the tuple format is (train no, dep. time, arrival time,fcp,scp)
        """

        #first, query for trains and their departure times that depart from departure station
        #parameters in the form Name(Location), parse to get Name
        departure_station = departure_station.split('(')[0]
        arrival_station = arrival_station.split('(')[0]
        cursor = self.db.cursor()
        sql = "SELECT TRAIN_NO, DEPARTURE_TIME FROM STOP WHERE name='%s'" % departure_station
        cursor = self.query(cursor, sql)[0]
        dep_stas = cursor.fetchall()

        listy_list = []
        temp = []

        for i in dep_stas:
            #using those trains we queried, find those that arrive at arrival station at a later time
            sql = "SELECT TRAIN_NO FROM STOP WHERE name='%s' AND TRAIN_NO='%d' AND ARRIVAL_TIME > '%s'" % (arrival_station, i[0], i[1])
            cursor = self.query(cursor, sql)[0]
            temp.append(cursor.fetchone())

        for j in temp:
            if (j):
                #get the departure time from those trains
                sql = "SELECT DEPARTURE_TIME FROM STOP WHERE Train_No='%d' AND Name='%s'" % (j[0], departure_station)
                cursor = self.query(cursor, sql)[0]
                dep_t = (cursor.fetchone())[0]
                #get the arrival time from those trains
                sql = "SELECT ARRIVAL_TIME FROM STOP WHERE Train_No='%d' AND Name='%s'" % (j[0], arrival_station)
                cursor = self.query(cursor, sql)[0]
                arr_t = (cursor.fetchone())[0]
                sql = "SELECT 1ST_CLASS_PRICE FROM TRAIN_ROUTE WHERE Train_No='%d'" % (j[0])
                cursor = self.query(cursor, sql)[0]
                f_class_price = cursor.fetchone()[0]
                sql = "SELECT 2ND_CLASS_PRICE FROM TRAIN_ROUTE WHERE Train_No='%d'" % (j[0])
                cursor = self.query(cursor, sql)[0]
                s_class_price = cursor.fetchone()[0]
                listy_list.append((j[0],dep_t,arr_t, f_class_price, s_class_price))

        return listy_list

    def find_card(self, username):
        """
        Returns a list of cards corresponding to the username
        """
        cursor = self.db.cursor()
        sql = "SELECT CARD_NUMBER FROM PAYMENT_INFO WHERE CARD_USERNAME='%s'" % username
        cursor = self.query(cursor, sql)[0]
        listy_list = []
        temp = cursor.fetchone()
        while temp:
            listy_list.append(temp[0])
            temp = cursor.fetchone()
        return listy_list

    def make_reservation(self, username, card_number):
        cursor = self.db.cursor()
        sql = "INSERT INTO RESERVATION (CARD_NO, USERNAME, IS_CANCELLED) VALUES ('%d', '%s', '0')" % (card_number, username)
        self.query(cursor, sql)

    def generate_rid(self, username, card_num, total_cost):
        cursor = self.db.cursor()
        sql1 = "INSERT INTO RESERVATION (CARD_NO, USERNAME, IS_CANCELLED, TOTAL_COST) "\
        "VALUES ('%d', '%s', '0', %d)" % ( card_num, username, total_cost)
        cursor = self.query(cursor, sql1)[0]
        return cursor.lastrowid

    def cancel_reservation(self, rid):
        cursor = self.db.cursor()
        cost = self.get_refund(rid)
        if cost == -1:
            return cost
        sql = "UPDATE RESERVATION SET IS_CANCELLED = 1, TOTAL_COST = '%d' WHERE RID = '%d'" % (cost, rid)
        cursor = self.query(cursor, sql)[0]
        sql = "DELETE FROM RESERVES WHERE RID = '%d'" % rid
        cursor = self.query(cursor, sql)[0]

    def get_refund(self, rid):
        sql = "SELECT DEPARTURE_DATE FROM RESERVES WHERE RID = '%d' ORDER BY DEPARTURE_DATE" % rid
        cursor = self.query(cursor, sql)[0]
        dep_date =  cursor.fetchone()
        sql = "SELECT TOTAL_COST FROM RESERVATION WHERE RID = '%d' AND IS_CANCELLED = '0'" % rid
        cursor = self.query(cursor, sql)[0]
        cost_fetch = cursor.fetchone()
        if cost_fetch:
            if (dep_date[0] - date.today() > timedelta(days = 7)):
                cost = (.8*cost) - 50
            elif (dep_date[0] - date.today() > timedelta(days = 1)):
                cost = (.5*cost) - 50
            else:
                return -1
            if cost < 0:
                cost = 0
            return cost
            sdfsfd
        return -1

    def get_max_bags(self):
        cursor = self.db.cursor()
        sql = "SELECT Max_Num_Bags FROM SYSTEM_INFO"
        cursor = self.query(cursor, sql)[0]
        return cursor.fetchone()

    def get_free_bags(self):
        cursor = self.db.cursor()
        sql = "SELECT Num_Free_Bags FROM SYSTEM_INFO"
        cursor = self.query(cursor, sql)[0]
        return cursor.fetchone()

    def get_discount(self):
        cursor = self.db.cursor()
        sql = "SELECT Student_Discount FROM SYSTEM_INFO"
        cursor = self.query(cursor, sql)[0]
        return cursor.fetchone()


    def get_change_fee(self):
        cursor = self.db.cursor()
        sql = "SELECT Change_Fee FROM SYSTEM_INFO"
        cursor = self.query(cursor, sql)[0]
        return cursor.fetchone()

    def add_review(self, comment, rating, train_no, username):
        """
        Return value 1 for success, none for failure (train_no not in db/invalid, or query failure)
        """

        cursor = self.db.cursor()
        sql = "INSERT INTO REVIEW (Comment, Rating, Train_No, Username) "\
        "VALUES('%s','%d','%d','%s')" % (comment, rating, train_no, username)
        return None if (self.query(cursor,sql)[1] != 0) else 1

    def view_review(self, train_no):
        """
        Return value is list of (rating, comment) tuples for that train_no
        """

        cursor = self.db.cursor()
        sql = "SELECT Rating, Comment FROM REVIEW WHERE Train_No = '%d'" % train_no
        cursor = self.query(cursor, sql)[0]
        return cursor.fetchall()

    def update_reservation(self,res_id, train_no, dep_date, total_cost):
        """
        Updates train ticket, returns None if res_id invalid, 1 if succesful update
        Note: dep_date must be formatted as string
        """

        cursor = self.db.cursor()
        if (not self.validate_res_id(res_id)): return None
        sql = "UPDATE RESERVES SET Departure_Date = '%s' WHERE RID = '%d' AND Train_No = '%d'" % (dep_date, res_id, train_no)
        self.query(cursor,sql)
        sql = "UPDATE RESERVATION SET Total_Cost = '%d' WHERE RID = '%d'" % (total_cost, res_id)
        self.query(cursor,sql)
        return 1


    def validate_res_id(self, res_id):
        """
        Return 1 if RID valid, None if RID invalid or is cancelled
        """
        cursor = self.db.cursor()
        sql = "SELECT RID FROM RESERVATION WHERE RID = '%d' AND is_Cancelled = 0" % res_id
        cursor = self.query(cursor,sql)[0]
        return 1 if cursor.fetchone() else None

    def get_train_tickets(self, res_id):
        """
        Returns train trickets for a specific reservation, None if invalid res_id
        Return value is a list of tuples w/ tuple in format:
        (Train_No, Class, Dep_Date, Pass_Name, Num_Bags, Dep_From, Arr_At, Dep_Time, Arr_Time, Class_Price)
        """

        if(not self.validate_res_id(res_id)):
            return None

        cursor = self.db.cursor()
        sql = "SELECT Train_No, Class, Departure_Date, Passenger_Name, Num_Bags, Departs_From, Arrives_At "\
        "FROM RESERVES WHERE RID = '%d'" % res_id
        cursor = self.query(cursor, sql)[0]
        train_tickets = list(cursor.fetchall())
        i = 0
        for ticket in train_tickets:
            #get departure time
            sql = "SELECT Departure_Time FROM STOP WHERE Train_No = '%d' and Name = '%s'" % (ticket[0], ticket[5])
            cursor = self.query(cursor, sql)[0]
            date = (cursor.fetchone())
            if (date): train_tickets[i] += date

            #get arrival time
            sql = "SELECT Arrival_Time FROM STOP WHERE Train_No = '%d' and Name = '%s'" % (ticket[0], ticket[6])
            cursor = self.query(cursor, sql)[0]
            date = (cursor.fetchone())
            if (date): train_tickets[i] += date

            #get class price
            if (ticket[1] == 1):
                sql = "SELECT 1st_Class_Price FROM TRAIN_ROUTE WHERE Train_No = '%d'" % ticket[0]
                cursor = self.query(cursor, sql)[0]
                train_tickets[i] += (cursor.fetchone())
            else:
                sql = "SELECT 2nd_Class_Price FROM TRAIN_ROUTE WHERE Train_No = '%d'" % ticket[0]
                cursor = self.query(cursor, sql)[0]
                train_tickets[i] += (cursor.fetchone())
        return train_tickets


    def revenue_report(self):
        cursor = self.db.cursor()
        curr_month = date.today().month
        curr_year = date.today().year
        sql = "SELECT RID FROM RESERVES R WHERE MONTH(DEPARTURE_DATE) = '%d' AND YEAR(DEPARTURE_DATE) = '%d' AND R.DEPARTURE_DATE IN (SELECT MIN( DEPARTURE_DATE ) FROM  RESERVES GROUP BY RID)" % (curr_month,curr_year)
        cursor = self.query(cursor, sql)[0]
        month_one = 0
        for i in cursor.fetchall():
            sql = "SELECT TOTAL_COST FROM RESERVATION WHERE RID = '%d'" % i[0]
            cursor = self.query(cursor, sql)[0]
            month_one += cursor.fetchone()[0]
        ex_month = curr_month - 1
        ex_year = curr_year
        if (ex_month == 0):
            ex_month = 12
            ex_year -= 1
        sql = "SELECT RID FROM RESERVES R WHERE MONTH(DEPARTURE_DATE) = '%d' AND YEAR(DEPARTURE_DATE) = '%d' AND R.DEPARTURE_DATE IN (SELECT MIN( DEPARTURE_DATE ) FROM  RESERVES GROUP BY RID)" % (ex_month,ex_year)
        cursor = self.query(cursor, sql)[0]
        month_two = 0

        for i in cursor.fetchall():
            sql = "SELECT TOTAL_COST FROM RESERVATION WHERE RID = '%d'" % i[0]
            cursor = self.query(cursor, sql)[0]
            month_two += cursor.fetchone()[0]

        former_month = ex_month - 1
        former_year = ex_year
        if (former_month == 0):
            former_month = 12
            former_year -= 1
        sql = "SELECT RID FROM RESERVES R WHERE MONTH(DEPARTURE_DATE) = '%d' AND YEAR(DEPARTURE_DATE) = '%d' AND R.DEPARTURE_DATE IN (SELECT MIN( DEPARTURE_DATE ) FROM  RESERVES GROUP BY RID)" % (former_month, former_year)
        cursor = self.query(cursor, sql)[0]
        month_three = 0

        for i in cursor.fetchall():
            sql = "SELECT TOTAL_COST FROM RESERVATION WHERE RID = '%d'" % i[0]
            cursor = self.query(cursor, sql)[0]
            month_one += cursor.fetchone()[0]
        # print month_one
        return ((curr_month, month_one), (ex_month, month_two), (former_month, month_three))

    def popular_report(self):
        """
        Calculates and returns the popular train report
        Return value is a list of 3 lists or None for error
        Each list is in the format (month num, list of train num, list of # reservations for each train)
        """

        cursor = self.db.cursor()
        curr_date = date.today()
        curr_month = str(curr_date).split('-')[1]
        curr_month = int(curr_month)
        prev_month = (curr_month) - 1
        prev_month2 = (curr_month) - 2

        if (prev_month == 0): prev_month = 12
        if (prev_month2 == 0): prev_month2 = 12
        elif (prev_month2 == -1): prev_month2 = 11


        report = []
        #In Reserves Table, there should never be RID that is cancelled
        sql1 = "SELECT Train_No, COUNT(*) FROM RESERVES WHERE Departure_Date Like \'%-0" + str(prev_month2) \
        + "-%' GROUP BY Train_No ORDER BY COUNT(*) desc limit 3"
        sql2 = "SELECT Train_No, COUNT(*) FROM RESERVES WHERE Departure_Date Like \'%-0" + str(prev_month) \
        + "-%' GROUP BY Train_No ORDER BY COUNT(*) desc limit 3"
        sql3 = "SELECT Train_No, COUNT(*) FROM RESERVES WHERE Departure_Date Like \'%-0" + str(curr_month) \
        + "-%' GROUP BY Train_No ORDER BY COUNT(*) desc limit 3"
        sqllist = [sql1, sql2, sql3]
        monthlist = [prev_month2, prev_month, curr_month]

        for i in range(0, 3):
            listy_list = [str(monthlist[i])]
            trainlist = []
            countlist = []
            cursor = self.query(cursor, sqllist[i])[0]
            for row in cursor:
                trainlist.append(row[0])
                countlist.append(row[1])
            listy_list.append(trainlist)
            listy_list.append(countlist)
            report.append(listy_list)
        return listy_list


    #unused
    def get_not_cancelled_rid(self):
        cursor = self.db.cursor()
        sql = "SELECT RID FROM RESERVATION WHERE NOT is_Cancelled = 1"
        cursor = self.query(cursor, sql)[0]
        return cursor.fetchall()

    def query(self, cursor, sql):
        """
        Returns value is the tuple: (cursor, error_code)
        """

        error_code = 0
        try:
            cursor.execute(sql)
            self.db.commit()
        except pymysql.err.IntegrityError as e:
            print (e)
            error_code = 1
        except:
            e = sys.exc_info()
            print (e)
            error_code = 2
        return (cursor, error_code)

DB_Connect()
