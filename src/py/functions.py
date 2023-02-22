#necessary imports ---------->
from classes import *
import mysql.connector as mysqlc

#functions ---------->
def login():
    """ Login credentials authentication """
    #ask for user credentials
    login_user = input("\nUser: ")
    login_passwd = input("Password: ")
    #try stablishing connection with the Data Base
    try:
        mysqlconnection = mysqlc.connect(user = login_user, password = login_passwd, database = 'hour_tracker', host = '127.0.0.1', port = 3306, raise_on_warnings = True)
    #on failed login attempt show feedback to user and recursively call login()
    except:
        print("Incorrect Login Credentials")
        return login()
    #on successful connection return mysql connector
    else:
        return mysqlconnection

def sign_up_users(mysqlconnection):
    """ Create teacher users or create student tuples in the Data Base """
    #sign up loop
    while True:
        #get user input 
        input_data = int(input("\n\tSign Up\n\n1.Student\n2.Teacher\n\nOption-> "))
        #exit sign_up_users
        if input_data == -1:
            break
        #sign up student
        elif input_data == 1:
            #get the necessary data to create a new student
            identifier = input("\n\nIdentifier: ")
            name = input("Name: ")
            second_name = input("Second Name: ")
            oh = input("Objective Hours: ")
            #create student object
            temp_student = Student(identifier, name, second_name, oh)
            #upload student to Data Base
            temp_student.upload_to_db(mysqlconnection)
        #sign up teacher
        elif input_data == 2:
            #get the necessary data to create a new teacher user
            identifier = input("\nIdentifier: ")
            password = input("Password: ")
            #create teacher object
            temp_teacher = Teacher(identifier, password)
            #create teacher user on the Data Base
            temp_teacher.create_db_user(mysqlconnection)
        #default for not expected input
        else:
            print("\nIncorrect Input")

def view_students(mysqlconnection):
    """ View teacher users or student tuples in the Data Base """
    #create cursor
    cursor = mysqlconnection.cursor()
    #query to be executed
    sql_query = "SELECT * FROM hour_tracker.student;"
    #execution of query
    cursor.execute(sql_query)
    #fetch query results
    result = cursor.fetchall()
    #close cursor
    cursor.close()
    #print all students from the Data Base
    for it in result:
        print(f"Student Identifier: {it[0]} | Student Name: {it[1]+' '+it[2]} | Objective Hours: {it[3]} | Current Hours: {it[4]}")

def delete_student(mysqlconnection):
    """ Delete student from Data Base """
    #create cursor
    cursor = mysqlconnection.cursor()
    #ask for the id of the student to be removed from the Data Base
    student_id = input("Student ID: ")
    #query to be executed
    sql_query = f"DELETE FROM `hour_tracker`.`student` WHERE (`id_user` = '{student_id}');"
    #execution of query
    cursor.execute(sql_query)
    #close cursor
    cursor.close()
    #commit changes on the Data Base
    mysqlconnection.commit()

def delete_teacher(mysqlconnection):
    """ Delete teacher user from Data Base """
    #if teacher doesn't exist it doesn't matter, no error will be thrown
    #create cursor
    cursor = mysqlconnection.cursor()
    #ask for the id of the teacher user to be removed from the Data Base
    teacher_id = input("Teacher ID: ")
    #query to be executed
    sql_query = f"DELETE FROM `mysql`.`user` WHERE (`Host` = 'localhost') and (`User` = '{teacher_id}');"
    #execution of query
    cursor.execute(sql_query)
    #close cursor
    cursor.close()
    #commit changes on the Data Base
    mysqlconnection.commit()

def user_management(mysqlconnection):
    """ Function that encapsulates all the user management functionalities """
    #user_management loop
    while True:
        #get user input
        input_data = int(input("\n\tUser Management Menu\n\n1.Sign Up Users\n2.View Students\n3.Delete Student\n4.Delete Teacher\n\nOption-> "))
        #exit user_management
        if input_data == -1:
            break
        #enter sign up section
        elif input_data == 1:
            sign_up_users(mysqlconnection)
        #enter hour checker section
        elif input_data == 2:
            view_students(mysqlconnection)
        #enter delete student section
        elif input_data == 3:
            delete_student(mysqlconnection)
        #enter delete teacher section
        elif input_data == 4:
            delete_teacher(mysqlconnection)
        #default for not expected input
        else:
            print("\nIncorrect Input")

def hour_tracker(mysqlconnection):
    """ Hour Tracker (main function of the program) """
    #stores the user input (user identifier or admin options)
    input_data = 0
    #dictionary to store all active students in the system
    student_dictionary = {}
    #dictionary to store all the registers on the session
    register_dictionary = {}
    #hour checker loop
    while True:
        #get user input
        input_data = int(input("\nUser Identifier-> "))
        #exit program
        if input_data == -1:
            break
        #print register_dictionary
        elif input_data == -2:
            for n in register_dictionary:
                register_dictionary[n].print_register()
        #student entering/exiting the system
        else:
            #student entering
            if register_dictionary.get(input_data) == None:
                #create student object with only its id
                student = Student(input_data)
                if student.check_if_user_exists(mysqlconnection,student_dictionary):
                    #append student entering register to register_dictionary
                    register_dictionary[input_data] = Register(input_data)
            #user exits
            else:
                print(f"Goodbye {input_data}")
                #get exit time
                register_dictionary[input_data].exit()
                #print the register of the exiting user
                register_dictionary[input_data].print_register()
                #upload the register to the data base
                register_dictionary[input_data].upload_to_db(mysqlconnection,student_dictionary[input_data])
                #pop the register of the exiting user
                register_dictionary.pop(input_data)

def system_start(mysqlconnection):
    """ Main Menu of program """
    #menu loop
    while True:
        #get user input
        input_data = int(input("\n\tMain Menu\n\n1.User Management\n2.Hour Tracker\n\nOption-> "))
        #exit program
        if input_data == -1:
            break
        #enter sign up section
        elif input_data == 1:
            user_management(mysqlconnection)
        #enter hour tracker section
        elif input_data == 2:
            hour_tracker(mysqlconnection)
        #default for not expected input
        else:
            print("\nIncorrect Input")
