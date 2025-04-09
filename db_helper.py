#At first, do pip install mysql-connector-python to install connector in GitBash
from typing import ContextManager

import mysql.connector
from contextlib import contextmanager

from logging_setup import setup_logger
logger=setup_logger('db_helper')

@contextmanager
def get_db_cursor(commit=False):       #commit-false, so that changes in database not saved
#establish connection to mysql workbench databse
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )
    #create cursor object to create queries
    cursor=connection.cursor(dictionary=True) #to get data in dictionary
    yield cursor
    if commit:  # if we want to save changes then commit true, then database saved changes
        connection.commit()
    cursor.close()
    connection.close()

def fetch_all_records():
    query="SELECT * from expenses"
    with get_db_cursor() as cursor:
        cursor.execute(query)  #execute query, if paramters have to passed also then check below function code

        expenses=cursor.fetchall() #fetch all rows from executed query
        return expenses
        #for expense in expenses: #print data
         #   print(expense)

def fetch_expense_date(date):
    logger.info(f"fetch expense for date called with {date}")
    query="SELECT * from expenses where expense_date= %s"
    with get_db_cursor() as cursor:
        cursor.execute(query,(date,)) #passed on parameter to query execution

        expenses=cursor.fetchall()
        return expenses
        #for expense in expenses:
         #   print(expense)

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert expense on date {expense_date} for amount: {amount}, category: {category}, notes: {notes}")
    query="INSERT INTO expenses(expense_date, amount, category, notes) VALUES (%s,%s,%s,%s)"
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query, (expense_date, amount, category, notes))


def delete_expense(expense_date):
    logger.info(f"insert expense on date {expense_date}")
    query="Delete from expenses where expense_date=%s "
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(query,(expense_date,))

def expenses_by_category(start_date,end_date):
    logger.info(f"fetch category wise exepnses from start date {start_date} and end_date {end_date}")
    query='''SELECT category, SUM(amount) as Total
            FROM expenses
            WHERE expense_date
            BETWEEN %s and %s
            GROUP BY category'''
    with get_db_cursor() as cursor:
        cursor.execute(query,(start_date, end_date))
        total_expenses=cursor.fetchall()
        return total_expenses
        #for category_wise_expense in total_expenses:
         #   print(category_wise_expense)
def expense_by_month():
    logger.info(f"fetch expense month wise")
    query='''WITH CTE1
            AS (SELECT amount, MONTH(expense_date) as month_number, MONTHNAME(expense_date)as month_name, expense_date  FROM expenses)
            SELECT month_name, sum(amount) as total, month_number FROM CTE1
            GROUP BY month_name, month_number
            ORDER BY total asc'''
    with get_db_cursor() as cursor:
        cursor.execute(query)
        total_expenses=cursor.fetchall()
        return total_expenses

#if __name__ == "__main__" :
    #fetch_all_records()
    #fetch_expense_date('2024-08-02')
    #insert_expense('2025-03-25','150','mobile','ONEPLUS')
    #delete_expense('2025-03-25')
    #fetch_expense_date('2025-03-25')
    #expenses_by_category("2024-08-01","2024-08-15")
    #expenses=expense_by_month()
    #for expense in expenses:
    #   print(expense)

