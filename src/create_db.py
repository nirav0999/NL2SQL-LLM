import os
from utils import dumpJsonFile, loadJsonFile, createSQLDB
import sqlite3

DB_FILEPATH = "../data/database/final_db.db"

earning_db_path = "../data/sql/earning.sql"
employee_db_path = "../data/sql/employee.sql"
employeepayrollrun_db_path = "../data/sql/employeepayrollrun.sql"
group_db_path = "../data/sql/group_final.sql"
payrollrun_db_path = "../data/sql/payrollrun.sql"
paygroup_db_path = "../data/sql/paygroup.sql"

conn = sqlite3.connect(DB_FILEPATH)

with open(earning_db_path, 'r') as sql_file:
    conn.executescript(sql_file.read())

with open(earning_db_path, 'r') as sql_file:
    conn.executescript(sql_file.read())

with open(employee_db_path, 'r') as sql_file:
    conn.executescript(sql_file.read())

with open(employeepayrollrun_db_path, 'r') as sql_file:
    conn.executescript(sql_file.read())

with open(group_db_path, 'r') as sql_file:
    conn.executescript(sql_file.read())

with open(payrollrun_db_path, 'r') as sql_file:
    conn.executescript(sql_file.read())

with open(paygroup_db_path, 'r') as sql_file:
    conn.executescript(sql_file.read())

conn.close()


