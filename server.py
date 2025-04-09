from fastapi import FastAPI, HTTPException
import db_helper
from datetime import date
from typing import List
from pydantic import BaseModel

app=FastAPI()

class Expense(BaseModel):
    amount:float
    category:str
    notes:str

class DateRange(BaseModel):
    start_date:date
    end_date:date

@app.get("/expense")
def fetch_all_expenses():
    expenses=db_helper.fetch_all_records()
    return expenses

@app.get("/expense_date/{expense_date}", response_model=List[Expense])
def fetch_expense_datewise(expense_date:date):
    expenses=db_helper.fetch_expense_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="failed to retrieve expenses from database")
    return expenses

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date,expenses:List[Expense]):
    db_helper.delete_expense(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date,expense.amount, expense.category, expense.notes)
    return "expense updated successfully"

@app.get("/category_wise_expense/{start_date}/{end_date}")
def category_wise_expense(date_range:DateRange):
    expenses=db_helper.expenses_by_category(date_range.start_date,date_range.end_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="failed to retrieve expenses from database")
    return expenses

@app.post("/analytics/")
def expense_analytics(date_range: DateRange):
    data=db_helper.expenses_by_category(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="failed to retrieve expenses from database")
    analytics={}
    total=sum([row['Total'] for row in data])
    for row in data:
        percentage=round((row['Total']/total)*100,2) if total!=0 else 0
        analytics[row['category']]={"Total": row['Total'], "percentage":percentage}
    return analytics

@app.get("/month_wise_expense")
def month_wise_expense():
    expense=db_helper.expense_by_month()
    if expense is None:
        raise HTTPException(status_code=500, detail="failed to retrieve error")
    return expense