#necessary imports ---------->
import datetime

#class definitions ---------->
#User class
class User:
    def __init__(self,identifier):
        """ User constructor """
        self.identifier = identifier

#Teacher class
class Teacher(User):
    def __init__(self, identifier, password=''):
        """ Teacher constructor """
        super().__init__(identifier)
        self.password = password
    def print_teacher(self):
        """ Print the student object in a human readable format """
        print(f"Teacher Identifier: {self.identifier} | Teacher Name: {self.username}")

    def create_db_user(self, mysqlconnection):
        """ Create Teacher user on the Data Base """
        #create cursor
        cursor = mysqlconnection.cursor()
        #query to be executed
        sql_query = f"CREATE USER IF NOT EXISTS '{self.identifier}'@'localhost' IDENTIFIED BY '{self.password}' DEFAULT ROLE teacher;"
        #execution of query
        cursor.execute(sql_query)
        #close cursor
        cursor.close()
        #commit changes on the Data Base
        mysqlconnection.commit()
        
#Student class
class Student(User):

    def __init__(self,identifier,name = '',second_name= '',objective_hours = 0):
        """ Student constructor """
        super().__init__(identifier)
        self.name = name
        self.second_name = second_name
        self.objective_hours = objective_hours
        self.current_hours = 0.0

    def print_student(self):
        """ Print the student object in a human readable format """
        print(f"Student Identifier: {self.identifier} | Student Name: {self.name+' '+self.second_name} | Objective Hours: {self.objective_hours} | Current Hours: {self.current_hours}")

    def upload_to_db(self, mysqlconnection):
        """ Upload Student to data base """
        #create cursor
        cursor = mysqlconnection.cursor()
        #query to be executed
        sql_query = f"INSERT INTO `hour_tracker`.`student` (`id_user`, `name`, `second_name`, `objective_hours`, `current_hours`) VALUES ('{self.identifier}', '{self.name}', '{self.second_name}', '{self.objective_hours}', '{self.current_hours}')"
        #execution of query
        cursor.execute(sql_query)
        #close cursor
        cursor.close()
        #commit changes on the Data Base
        mysqlconnection.commit()

    def check_if_user_exists(self,mysqlconnection,student_dictionary):
        """ Check if the indicated user exists in the data base """
        #create cursor
        cursor = mysqlconnection.cursor()
        #query to be executed
        sql_query = f"SELECT * FROM hour_tracker.student WHERE (id_user = {self.identifier});"
        #execution of query
        cursor.execute(sql_query)
        #fetch query results
        result = cursor.fetchall()
        #close cursor
        cursor.close()
        #if result contains one tuple, the student is in the Data Base
        if len(result):
            #initialize the student object with its corresponding data
            self.name = result[0][1]
            self.second_name = result[0][2]
            self.objective_hours = result[0][3]
            self.current_hours = result[0][4]
            self.print_student()
            student_dictionary[self.identifier] = self
            return 1
        #case where list is empty, meaning the student isn't on the Data Base
        else:
            print("ID not found in the Data Base")
            return 0

    def update_current_hours_on_db(self,mysqlconnection):
        """ Update Student from data base """
        #create cursor
        cursor = mysqlconnection.cursor()
        #query to be executed
        sql_query = f"UPDATE `hour_tracker`.`student` SET `current_hours` = '{self.current_hours}' WHERE (`id_user` = '{self.identifier}')"
        #execution of query
        cursor.execute(sql_query)
        #close cursor
        cursor.close()
        #commit changes on the Data Base
        mysqlconnection.commit()

#Register class
class Register:
    def __init__(self, user_identifier):
        """ Register constructor """
        self.user_identifier = user_identifier
        self.enter_hour = datetime.datetime.now()
        self.exit_hour = None
    
    def exit(self):
        """ Saves exit hour of the user """
        self.exit_hour = datetime.datetime.now()
    
    def print_register(self):
        """ Prints the Register object in a human readable format """
        print(f"User_Identifier: {self.user_identifier} | Enter Hour: {self.enter_hour} | Exit Hour: {self.exit_hour}")

    def upload_to_db(self, mysqlconnection, student):
        """ Upload Register to the data base """
        #create cursor
        cursor = mysqlconnection.cursor()
        #query to be executed
        sql_query = f"INSERT INTO `hour_tracker`.`register` (`fk_id_user`, `enter_hour`, `exit_hour`) VALUES ('{self.user_identifier}', '{self.enter_hour.strftime('%Y-%m-%d %H:%M:%S')}', '{self.exit_hour.strftime('%Y-%m-%d %H:%M:%S')}');"
        #execution of query
        cursor.execute(sql_query)
        #update current hours of the exiting student
        student.current_hours += (float(self.exit_hour.hour) + float(self.exit_hour.minute / 60)) - (float(self.enter_hour.hour) + float(self.enter_hour.minute / 60))
        #update current hours of student in the Data Base
        student.update_current_hours_on_db(mysqlconnection)
        #close cursor
        cursor.close()
        #commit changes on the Data Base
        mysqlconnection.commit()
