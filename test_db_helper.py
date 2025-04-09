
import os
import sys
import pytest
from backend import db_helper

def test_fetch_all_record():
    expenses0=db_helper.fetch_all_records()
    assert len(expenses0)==60

def test_fetch_expense_date():
    expenses1=db_helper.fetch_expense_date("2024-08-01")
    assert expenses1[0]['id']==63
    assert expenses1[0]['amount']==1227
    assert expenses1[0]['category']=='Rent'

def test_fetch_expense_invalid_date():
    expenses2=db_helper.fetch_expense_date("9999-5-01")
    assert len(expenses2)==0

def test_expense_by_category_invalid_dates():
    expenses3=db_helper.expenses_by_category("9999-05-01", "9999-08-01")
    assert len(expenses3)==0

def test_monthwise_expense():
    expense4=db_helper.expense_by_month()
    assert len(expense4)==4
#Test driven development(TDD)


