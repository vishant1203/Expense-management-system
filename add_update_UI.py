import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import json

from streamlit import header

API_URL="http://127.0.0.1:8000" #localhost: 127.0.0.1

st.title("Expense Management System")
tab1,tab2=st.tabs(["Add/Update","Analytics"]) #creation of tabs




with tab1:
    def add_update_UI():
        selected_date=st.date_input("Enter Date" , datetime(2024,8,2), label_visibility="collapsed") # datetime used to set default value of date
        response=requests.get(f"{API_URL}/expense_date/{selected_date}") #calling API using request library
        if response.status_code==200:
            existing_expenses=response.json()      #parsing json data
            #st.write(existing_expenses)
        else:
            st.error("failed to retrieve any data")
            existing_expenses=[]
        categories=["Rent", "Food", "Shopping", "Entertainment", "Other"]
        with st.form(key="expense_form"): # form is used to make table and key name to specify name to that particular form
            col1, col2,col3=st.columns(3)
            with col1:
                st.text("Amount")
            with col2:
                st.text("Category")
            with col3:
                st.text("Notes")
            expenses=[]
            for i in range(10):
                if i<len(existing_expenses):
                    amount=existing_expenses[i]['amount']
                    category=existing_expenses[i]['category']
                    notes=existing_expenses[i]['notes']
                else:
                    amount=0.0
                    category="Other"
                    notes=''
                col1, col2, col3=st.columns(3)
                with col1:
                    number_input=st.number_input(label='Amount',min_value=0.0, step=1.0, value=amount, key=f"amount_{i}", label_visibility="collapsed") # 1. value is deafult value. 2. min, step and value should have same type 3. should have specific key always to identify
                    # value=amount
                with col2:
                    category_input=st.selectbox(label='Category', index=categories.index(category), options=categories, key=f"category_{i}", label_visibility="collapsed")
                    #INDEX used to set values for DROPDOWN objects otherwise if not drodown then use value=" "
                with col3:
                    notes_input=st.text_input( label='Notes', value=notes, key=f"notes_{i}", label_visibility="collapsed")
                    #value=notes
                expenses.append(
                {'amount':number_input,
                 'category':category_input,
                 'notes':notes_input}
                )

            submit_button=st.form_submit_button()
            if submit_button:
                filtered_expenses=[expense for expense in expenses if expense['amount']>0]
                response1=requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
                if response1.status_code==200:
                    st.success("Expenses updated succesfully")
                else:
                    st.error("Failed to update expenses:")