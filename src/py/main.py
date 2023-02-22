"""-----------------------------------------------------------------------------------------------------------------------------------
- Software Name: Student Hour Tracker
- Version: 1.0
- Language: Python
- Developer: Emilio Rivera Macías
- Date: February 21, 2023
- Contact: emilioriveramacias@gmail.com
-----------------------------------------------------------------------------------------------------------------------------------"""

"""-----------------------------------------------------------------------------------------------------------------------------------
Version Notes:
    - This version is developed to only monitor the hours of work in the same day, so if someone enters the system one day and 
    exits it the next day this would couse unexpected results since the hour difference only takes in count hours and minuts and
    not days or months
    - This program is developed to work with barcode scanners that behave like keyboards, so no extra configuration is needed
    to start working with this hardware
    - This program is developed to work with MySQL, but with a few little changes it can work with any other SQL Data Base
-----------------------------------------------------------------------------------------------------------------------------------"""

"""-----------------------------------------------------------------------------------------------------------------------------------
Notes for Next Versions:
    - implement the GUI
-----------------------------------------------------------------------------------------------------------------------------------"""

#necessary imports ---------->
from functions import *

#procedure ---------->
#login
mysqlconnection = login()
#main menu
system_start(mysqlconnection)
#close connection
mysqlconnection.close()
